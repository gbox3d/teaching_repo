import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';
const root=fileURLToPath(new URL('../../../specials/synthesizer/', import.meta.url));
const walk=async dir=>(await Promise.all((await fs.readdir(dir,{withFileTypes:true})).map(d=>d.isDirectory()?walk(path.join(dir,d.name)):path.join(dir,d.name)))).flat();
const files=await walk(root);let syntax=0;const missing=[];
for(const f of files){const s=await fs.readFile(f,'utf8');if(f.endsWith('.js')){execFileSync(process.execPath,['--check',f]);syntax++;}
 if(f.endsWith('.html'))for(const m of s.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)){if(!m[2].trim())continue;const temp=path.join(process.env.TEMP,'synth-inline-check'+(m[1].includes('module')?'.mjs':'.js'));await fs.writeFile(temp,m[2]);execFileSync(process.execPath,['--check',temp]);syntax++;}
 if(f.endsWith('.md'))for(const m of s.matchAll(/\]\(([^)]+)\)/g)){const ref=m[1];if(/^https?:|^#/.test(ref))continue;const dest=decodeURIComponent(ref.split('#')[0]);try{await fs.access(path.resolve(path.dirname(f),dest));}catch{missing.push({file:path.relative(root,f),ref});}}
 if(f.endsWith('.json'))JSON.parse(s);
}
console.log(JSON.stringify({files:files.map(f=>path.relative(root,f).replaceAll('\\','/')),syntax,missing},null,2));
if(missing.length)process.exitCode=1;
const browser=await chromium.launch({channel:'chrome',headless:true});const page=await browser.newPage({viewport:{width:375,height:900}});
for(const [name,file] of [['envelope','ex03_envelope.html'],['pattern','ex08_pattern.html'],['player','build/index.html'],['composer','build/compose.html']]){await page.goto('http://localhost:8111/specials/synthesizer/examples/'+file);await page.waitForTimeout(200);await page.screenshot({path:path.join(process.env.TEMP,'synth-'+name+'.png'),fullPage:true});}
await browser.close();
