import assert from 'node:assert/strict';
import test from 'node:test';

import { createCollaborationBridge } from '../js/collaboration-bridge.js';

test('publishes an immutable shared and human-only capability contract', () => {
  const bridge = createCollaborationBridge({
    getState: () => ({ angle: 0 }),
    commands: {
      rotate: () => ({ summary: 'Rotated image' }),
    },
  });

  assert.equal(bridge.version, '1.0.0');
  assert.equal(Object.isFrozen(bridge), true);
  assert.equal(Object.isFrozen(bridge.capabilities), true);
  assert.deepEqual(bridge.capabilities.commands, [
    {
      id: 'rotate',
      access: 'human-ai',
      callable: true,
      reversible: true,
    },
  ]);
  assert.deepEqual(
    bridge.capabilities.protected.map(({ id, access, callable }) => ({
      id,
      access,
      callable,
    })),
    [
      { id: 'gps-permission', access: 'human-only', callable: false },
      { id: 'file-selection', access: 'human-only', callable: false },
      { id: 'download', access: 'human-only', callable: false },
    ],
  );
  assert.equal(Object.isFrozen(bridge.capabilities.protected[0]), true);
});

test('executes an allowed command and emits one deterministic activity record', async () => {
  const activities = [];
  const events = [];
  const state = { angle: 0 };
  const eventTarget = {
    dispatchEvent(event) {
      events.push(event);
      return true;
    },
  };
  const bridge = createCollaborationBridge({
    getState: () => ({ ...state }),
    commands: {
      rotate({ degrees }, context) {
        assert.deepEqual(context, { actor: 'ai', command: 'rotate' });
        state.angle = degrees;
        return { summary: `Rotated to ${degrees} degrees` };
      },
    },
    onActivity: (activity) => activities.push(activity),
    eventTarget,
    now: () => new Date('2026-08-26T04:00:00.000Z'),
  });

  const currentState = await bridge.execute('rotate', { degrees: 90 });

  assert.deepEqual(currentState, { angle: 90 });
  assert.deepEqual(activities, [
    {
      actor: 'ai',
      command: 'rotate',
      status: 'success',
      summary: 'Rotated to 90 degrees',
      timestamp: '2026-08-26T04:00:00.000Z',
    },
  ]);
  assert.equal(Object.isFrozen(activities[0]), true);
  assert.equal(events[0].type, 'collaboration-activity');
  assert.equal(events[0].detail, activities[0]);
});

test('accepts a human actor and an explicit concise summary', async () => {
  let activity;
  const bridge = createCollaborationBridge({
    getState: () => ({ brightness: 110 }),
    commands: { setBrightness: () => 'handler summary' },
    onActivity: (entry) => {
      activity = entry;
    },
    now: () => '2026-08-26T04:01:00.000Z',
  });

  await bridge.execute(
    'setBrightness',
    { value: 110 },
    { actor: 'human', summary: 'Brightness changed to 110%' },
  );

  assert.deepEqual(activity, {
    actor: 'human',
    command: 'setBrightness',
    status: 'success',
    summary: 'Brightness changed to 110%',
    timestamp: '2026-08-26T04:01:00.000Z',
  });
});

test('rejects and records unknown and protected command requests', async () => {
  let calls = 0;
  const activities = [];
  const bridge = createCollaborationBridge({
    getState: () => ({}),
    commands: {
      rotate: () => {
        calls += 1;
      },
    },
    onActivity: (activity) => activities.push(activity),
    now: () => '2026-08-26T04:02:00.000Z',
  });

  await assert.rejects(
    bridge.execute('missing'),
    (error) => error.code === 'UNKNOWN_COMMAND',
  );
  await assert.rejects(
    bridge.execute('gps-permission'),
    (error) => error.code === 'PROTECTED_COMMAND',
  );
  await assert.rejects(
    bridge.execute('file-selection', undefined, { actor: 'human' }),
    (error) => error.code === 'PROTECTED_COMMAND',
  );
  await assert.rejects(
    bridge.execute('download'),
    (error) => error.code === 'PROTECTED_COMMAND',
  );
  await assert.rejects(
    bridge.execute('rotate', undefined, { actor: 'service' }),
    (error) => error.code === 'INVALID_ACTOR',
  );
  assert.equal(calls, 0);
  assert.deepEqual(
    activities.map(({ actor, command, status }) => ({ actor, command, status })),
    [
      { actor: 'ai', command: 'missing', status: 'failure' },
      { actor: 'ai', command: 'gps-permission', status: 'failure' },
      { actor: 'human', command: 'file-selection', status: 'failure' },
      { actor: 'ai', command: 'download', status: 'failure' },
    ],
  );
});

test('records handler failures and serializes concurrent commands', async () => {
  const activities = [];
  const order = [];
  let releaseFirst;
  const firstGate = new Promise((resolve) => {
    releaseFirst = resolve;
  });
  const bridge = createCollaborationBridge({
    getState: () => ({ order: [...order] }),
    commands: {
      async first() {
        order.push('first:start');
        await firstGate;
        order.push('first:end');
      },
      second() {
        order.push('second');
        throw new Error('planned failure');
      },
    },
    onActivity: (activity) => activities.push(activity),
    now: () => '2026-08-26T04:03:00.000Z',
  });

  const first = bridge.execute('first');
  const second = bridge.execute('second');
  await Promise.resolve();
  assert.deepEqual(order, ['first:start']);
  releaseFirst();

  await first;
  await assert.rejects(second, /planned failure/);
  assert.deepEqual(order, ['first:start', 'first:end', 'second']);
  assert.deepEqual(
    activities.map(({ command, status }) => ({ command, status })),
    [
      { command: 'first', status: 'success' },
      { command: 'second', status: 'failure' },
    ],
  );
});

test('does not permit protected capabilities to be registered as commands', () => {
  assert.throws(
    () =>
      createCollaborationBridge({
        getState: () => ({}),
        commands: { download: () => {} },
      }),
    (error) => error.code === 'PROTECTED_COMMAND',
  );
});

test('publishes explicit non-reversible command metadata', () => {
  const bridge = createCollaborationBridge({
    getState: () => ({}),
    commands: {
      replaceImage: {
        reversible: false,
        handler: () => ({ summary: 'Image replaced' }),
      },
    },
  });

  assert.deepEqual(bridge.capabilities.commands, [
    {
      id: 'replaceImage',
      access: 'human-ai',
      callable: true,
      reversible: false,
    },
  ]);
});
