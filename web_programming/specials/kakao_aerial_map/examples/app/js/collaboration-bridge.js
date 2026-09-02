const VERSION = '1.0.0';
const ACTIVITY_EVENT = 'collaboration-activity';

const PROTECTED_CAPABILITIES = Object.freeze([
  Object.freeze({
    id: 'gps-permission',
    label: 'GPS permission',
    access: 'human-only',
    callable: false,
  }),
  Object.freeze({
    id: 'file-selection',
    label: 'File selection',
    access: 'human-only',
    callable: false,
  }),
  Object.freeze({
    id: 'download',
    label: 'Download',
    access: 'human-only',
    callable: false,
  }),
]);

const PROTECTED_COMMANDS = new Set(
  PROTECTED_CAPABILITIES.map(({ id }) => id),
);

function commandError(message, code) {
  const error = new Error(message);
  error.code = code;
  return error;
}

function toTimestamp(value) {
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) {
    throw new TypeError('now() must return a valid Date or date value.');
  }
  return date.toISOString();
}

function conciseSummary(command, suppliedSummary, result) {
  const candidate = suppliedSummary ?? result?.summary ?? result;
  const text = typeof candidate === 'string' ? candidate.trim() : '';
  const fallback = `${command} completed`;
  const summary = text || fallback;
  return summary.length > 160 ? `${summary.slice(0, 157)}...` : summary;
}

function createActivityEvent(detail) {
  if (typeof CustomEvent === 'function') {
    return new CustomEvent(ACTIVITY_EVENT, { detail });
  }

  if (typeof Event === 'function') {
    const event = new Event(ACTIVITY_EVENT);
    Object.defineProperty(event, 'detail', { value: detail });
    return event;
  }

  return Object.freeze({ type: ACTIVITY_EVENT, detail });
}

function failureSummary(command, error) {
  const message = error instanceof Error ? error.message : String(error);
  return conciseSummary(command, undefined, `${command} 실패: ${message}`);
}

export function createCollaborationBridge({
  getState,
  commands = {},
  onActivity,
  eventTarget,
  now = () => new Date(),
} = {}) {
  if (typeof getState !== 'function') {
    throw new TypeError('getState must be a function.');
  }
  if (!commands || typeof commands !== 'object' || Array.isArray(commands)) {
    throw new TypeError('commands must be an object of command functions.');
  }
  if (onActivity !== undefined && typeof onActivity !== 'function') {
    throw new TypeError('onActivity must be a function when supplied.');
  }
  if (typeof now !== 'function') {
    throw new TypeError('now must be a function.');
  }

  const commandEntries = Object.entries(commands).map(([name, definition]) => {
    if (PROTECTED_COMMANDS.has(name)) {
      throw commandError(
        `Protected command cannot be registered: ${name}`,
        'PROTECTED_COMMAND',
      );
    }
    if (!name.trim()) {
      throw new TypeError('Each command must have a name.');
    }

    const descriptor =
      typeof definition === 'function'
        ? { handler: definition, reversible: true }
        : definition;
    if (!descriptor || typeof descriptor.handler !== 'function') {
      throw new TypeError('Each command must have a function handler.');
    }
    if (
      descriptor.reversible !== undefined &&
      typeof descriptor.reversible !== 'boolean'
    ) {
      throw new TypeError('Command reversible metadata must be boolean.');
    }

    return {
      name,
      handler: descriptor.handler,
      reversible: descriptor.reversible ?? true,
    };
  });

  const handlers = new Map(
    commandEntries.map(({ name, handler }) => [name, handler]),
  );
  const capabilities = Object.freeze({
    commands: Object.freeze(
      commandEntries.map(({ name: id, reversible }) =>
        Object.freeze({
          id,
          access: 'human-ai',
          callable: true,
          reversible,
        }),
      ),
    ),
    protected: PROTECTED_CAPABILITIES,
  });

  const target =
    eventTarget ??
    (typeof globalThis.dispatchEvent === 'function' ? globalThis : null);

  let commandQueue = Promise.resolve();

  function publishActivity({ actor, command, summary, status }) {
    const activity = Object.freeze({
      actor,
      command,
      status,
      summary,
      timestamp: toTimestamp(now()),
    });

    onActivity?.(activity);
    if (target && typeof target.dispatchEvent === 'function') {
      target.dispatchEvent(createActivityEvent(activity));
    }
  }

  async function performExecute(command, payload, options) {
    const actor = options.actor ?? 'ai';
    if (actor !== 'ai' && actor !== 'human') {
      throw commandError(
        `Unsupported actor: ${actor}`,
        'INVALID_ACTOR',
      );
    }

    try {
      if (PROTECTED_COMMANDS.has(command)) {
        throw commandError(
          `사람이 직접 실행해야 하는 보호 기능입니다: ${command}`,
          'PROTECTED_COMMAND',
        );
      }

      const handler = handlers.get(command);
      if (!handler) {
        throw commandError(`허용되지 않은 공동 작업 명령입니다: ${command}`, 'UNKNOWN_COMMAND');
      }

      const result = await handler(payload, { actor, command });
      const state = getState();
      publishActivity({
        actor,
        command,
        status: 'success',
        summary: conciseSummary(command, options.summary, result),
      });
      return state;
    } catch (error) {
      publishActivity({
        actor,
        command,
        status: 'failure',
        summary: failureSummary(command, error),
      });
      throw error;
    }
  }

  function execute(command, payload, options = {}) {
    const operation = commandQueue.then(() =>
      performExecute(command, payload, options ?? {}),
    );
    commandQueue = operation.catch(() => undefined);
    return operation;
  }

  return Object.freeze({
    version: VERSION,
    capabilities,
    getState,
    execute,
  });
}
