import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const base='http://localhost:8111/specials/synthesizer/examples/';
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext();
await context.addInitScript(()=>{
 window.__starts=0;
 const originalStart=OscillatorNode.prototype.start;
 OscillatorNode.prototype.start=function(...args){window.__starts++;return originalStart.apply(this,args);};
 const originalResume=AudioContext.prototype.resume;
 AudioContext.prototype.resume=async function(...args){await originalResume.apply(this,args);await new Promise(r=>setTimeout(r,200));};
});
const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
for(const name of ['index','compose']){
 await page.goto(base+'build/'+name+'.html');await page.waitForSelector(name==='index'?'#sheet .bar':'#arrangement .bar');
 await page.locator('#play').click();await page.locator('#stop').click();await page.waitForTimeout(350);
 assert.equal(await page.evaluate(()=>__starts),0);assert.equal(await page.locator('#where').textContent(),'정지');
}
await page.goto(base+'build/index.html');await page.waitForSelector('#sheet .bar');
await page.route('**/my_song.json',async r=>{await new Promise(r=>setTimeout(r,400));await r.fulfill({status:404,body:'missing'});});
await page.locator('#song').selectOption('my_song.json');await page.locator('#song').selectOption('only_you.json');await page.waitForTimeout(600);
assert.equal(await page.locator('#sheet .bar').count(),28);assert.equal(await page.locator('#message').textContent(),'');
const requests=[];for(const [file,status] of [['ex09_song.json',200],['build/my_song.json',200],['missing-song.json',404]]){const r=await fetch(base+file,{headers:{Accept:'application/json'}});assert.equal(r.status,status);requests.push({file,status:r.status,contentType:r.headers.get('content-type')});}
assert.deepEqual(errors,[]);
const result={cancelPendingResume:['player','composer'],staleFailureIgnored:true,requests,errors};
await fs.writeFile(process.env.TEMP+'/synth-edge-result.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));await browser.close();
