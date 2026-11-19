import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
const base='http://localhost:8111/specials/synthesizer/examples/';
const result={browser:'',viewports:[],functions:[],errors:[]};
const browser=await chromium.launch({channel:'chrome',headless:true}); result.browser=browser.version();
const context=await browser.newContext({acceptDownloads:true});
await context.addInitScript(()=>{
 window.__audio={contexts:[],starts:[],stops:[],disconnects:0};
 const Native=window.AudioContext;
 window.AudioContext=class extends Native {
  constructor(...args){super(...args);window.__audio.contexts.push(this);}
  createOscillator(){return track(super.createOscillator(),'osc');}
  createBufferSource(){return track(super.createBufferSource(),'buffer');}
  createGain(){const n=super.createGain(),d=n.disconnect.bind(n);n.disconnect=(...a)=>{window.__audio.disconnects++;return d(...a);};return n;}
 };
 function track(n,type){for(const key of ['start','stop']){const f=n[key].bind(n);n[key]=(...a)=>{window.__audio[key==='start'?'starts':'stops'].push({type,time:a[0]??0});return f(...a);};} return n;}
});
const page=await context.newPage();
page.on('pageerror',e=>result.errors.push(e.message));
const names=['ex01_wave.html','ex02_pitch.html','ex03_envelope.html','ex04_chord.html','ex05_filter.html','ex06_drums.html','ex07_timing.html','ex08_pattern.html','ex09_fetch_song.html','ex10_melody.html','build/index.html','build/compose.html'];
for(const width of [375,1280]){
 await page.setViewportSize({width,height:900});
 for(const name of names){
  await page.goto(base+name); await page.waitForTimeout(100);
  if(name==='build/index.html')await page.waitForSelector('#sheet .bar');
  if(name==='build/compose.html')await page.waitForSelector('#arrangement .bar');
  const sizes=await page.evaluate(()=>({body:document.documentElement.scrollWidth,viewport:innerWidth}));
  result.viewports.push({name,width,...sizes});assert.ok(sizes.body<=width,`overflow ${name} ${width}: ${sizes.body}`);
 }
}
await page.setViewportSize({width:1280,height:900});
for(const name of names.slice(0,6)){
 await page.goto(base+name); const buttons=page.locator('button');const count=await buttons.count();
 for(let i=0;i<count;i++)await buttons.nth(i).click();
 const audio=await page.evaluate(()=>({starts:__audio.starts.length,states:__audio.contexts.map(c=>c.state)}));
 assert.ok(audio.starts>=count, name);assert.deepEqual(audio.states,['running']);
 if(name==='ex02_pitch.html')assert.match(await page.locator('#info').textContent(),/523.3/);
 result.functions.push({name,buttons:count,...audio});
}
await page.goto(base+'ex07_timing.html');await page.locator('#bpm').fill('0');await page.locator('#b1').click();assert.equal(await page.evaluate(()=>__audio.starts.length),0);
await page.locator('#bpm').fill('109');await page.locator('#b2').click();assert.equal(await page.locator('#b1').isDisabled(),true);await page.waitForFunction(()=>!document.querySelector('#b2').disabled);
assert.equal(await page.evaluate(()=>__audio.starts.length),16);result.functions.push({name:'ex07',result:await page.locator('#result').textContent(),invalidBpm:'blocked',duplicate:'disabled'});
await page.locator('#busy').check();await page.locator('#b1').click();await page.waitForFunction(()=>!document.querySelector('#b1').disabled);result.functions.push({name:'ex07 CPU load callback intervals',result:await page.locator('#result').textContent()});
await page.goto(base+'ex08_pattern.html');await page.locator('#clear').click();assert.equal(await page.locator('#grid input:checked').count(),0);await page.locator('#grid input').first().check();await page.locator('#play').click();await page.waitForTimeout(180);assert.ok(await page.evaluate(()=>__audio.starts.length)>0);await page.locator('#stop').click();assert.equal(await page.locator('#status').textContent(),'정지');await page.locator('#rock').click();await page.locator('#disco').click();result.functions.push({name:'ex08',presets:'clear/rock/disco',editing:true,replay:true});
await page.goto(base+'ex09_fetch_song.html');await page.locator('#load').click();await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('200'));assert.equal(await page.locator('#v1').textContent(),'연습곡');
await page.route('**/ex09_song.json',r=>r.fulfill({status:404,body:'missing'}));await page.locator('#load').click();await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('404'));assert.equal(await page.locator('#v1').textContent(),'');await page.unroute('**/ex09_song.json');await page.locator('#load').click();await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('200'));result.functions.push({name:'ex09',success:true,failure404Clears:true,recovery:true});
await page.goto(base+'ex10_melody.html');for(const id of ['b1','b2','b3'])await page.locator('#'+id).click();await page.locator('#stop').click();assert.equal(await page.evaluate(()=>__audio.starts.length),90);assert.equal(await page.evaluate(()=>__audio.stops.length),180);result.functions.push({name:'ex10',modes:3,notesPerMode:30,explicitStop:true});
await page.goto(base+'build/index.html');await page.waitForSelector('#sheet .bar');assert.equal(await page.locator('#sheet .bar').count(),28);
for(let i=0;i<3;i++){await page.locator('#play').click();await page.waitForTimeout(180);await page.locator('#stop').click();await page.waitForTimeout(340);}
assert.equal(await page.evaluate(()=>__audio.disconnects),3);result.functions.push({name:'player',cycles:3,outputDisconnected:3,states:await page.evaluate(()=>__audio.contexts.map(c=>c.state))});
await page.route('**/my_song.json',async r=>{await new Promise(r=>setTimeout(r,450));await r.continue();});await page.locator('#song').selectOption('my_song.json');await page.locator('#song').selectOption('only_you.json');await page.waitForTimeout(650);assert.match(await page.locator('#track').textContent(),/Only You/);assert.equal(await page.locator('#sheet .bar').count(),28);await page.unroute('**/my_song.json');
await page.route('**/my_song.json',r=>r.fulfill({status:200,contentType:'application/json',body:'{broken'}));await page.locator('#song').selectOption('my_song.json');await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('불러오지'));assert.equal(await page.locator('#sheet .bar').count(),0);assert.equal(await page.locator('#play').isDisabled(),true);await page.unroute('**/my_song.json');await page.locator('#song').selectOption('only_you.json');await page.waitForSelector('#sheet .bar');result.functions.push({name:'player JSON',latestRequestWins:true,invalidJsonClears:true,recovery:true});
await page.goto(base+'build/compose.html');await page.waitForSelector('#arrangement .bar');assert.equal(await page.locator('#arrangement .bar').count(),28);
const song={track_info:{title:'Research test',bpm:109,key:'C',artist:'student',time_signature:'4/4'},sections:[{section:'A',progression:[{bar:1,chord:'C',melody:[{step:1,midi:126,duration_steps:2}]},{bar:2,chord:'Am'}]}]};
await page.locator('#file-open').setInputFiles({name:'research.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(song))});await page.waitForFunction(()=>document.querySelector('#title').value==='Research test');
await page.locator('#arrangement .bar').first().click();await page.locator('#ed-chord').fill('invalid');await page.locator('#ed-chord').blur();assert.equal(await page.locator('#ed-chord').inputValue(),'C');
await page.locator('#ed-shift').fill('2');await page.locator('#ed-shift').blur();assert.equal(await page.locator('#ed-shift').inputValue(),'0');
await page.locator('#ed-shift').fill('-2');await page.locator('#ed-shift').blur();await page.locator('#ed-copy').click();assert.equal(await page.locator('#arrangement .bar').count(),3);await page.locator('#ed-right').click();await page.locator('#ed-left').click();await page.locator('#ed-delete').click();assert.equal(await page.locator('#arrangement .bar').count(),2);
const downloadPromise=page.waitForEvent('download');await page.locator('#export').click();const download=await downloadPromise;const json=JSON.parse(await fs.readFile(await download.path(),'utf8'));assert.equal(json.sections[0].progression[0].melody[0].midi,124);
await page.locator('#file-open').setInputFiles({name:'broken.json',mimeType:'application/json',buffer:Buffer.from('{bad')});await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('불러오지'));assert.equal(await page.locator('#arrangement .bar').count(),2);assert.equal(await page.locator('#title').inputValue(),'Research test');
await page.locator('#file-open').setInputFiles({name:'roundtrip.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(json))});await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('불러오기 완료'));
for(let i=0;i<3;i++){await page.locator('#play').click();await page.waitForTimeout(160);await page.locator('#stop').click();await page.waitForTimeout(330);}
result.functions.push({name:'composer',editRestore:true,midiBoundRestore:true,copyMoveDelete:true,exportReload:true,invalidJsonPreserves:true,cycles:3,outputDisconnected:await page.evaluate(()=>__audio.disconnects)});
await page.route('**/only_you.json',async r=>{await new Promise(r=>setTimeout(r,500));await r.continue();});await page.reload();await page.locator('#file-open').setInputFiles({name:'research.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(song))});await page.waitForTimeout(700);assert.equal(await page.locator('#title').inputValue(),'Research test');assert.equal(await page.locator('#arrangement .bar').count(),2);result.functions.push({name:'composer startup race',localFileWins:true});
assert.deepEqual(result.errors,[]);
await fs.writeFile(process.env.TEMP+'/synth-qa-result.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));await browser.close();
