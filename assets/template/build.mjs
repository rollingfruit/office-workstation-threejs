import {build} from 'esbuild';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
const result=await build({entryPoints:['src/main.js'],bundle:true,minify:true,format:'iife',write:false,target:['chrome110'],legalComments:'inline'});
const html=readFileSync('src/shell.html','utf8').replaceAll('__REFERENCE__','data:image/png;base64,'+readFileSync('reference.png').toString('base64')).replace('__BUNDLE__',()=>result.outputFiles[0].text.replaceAll('</script','<\\/script'));
mkdirSync('dist',{recursive:true});writeFileSync('dist/workstation.html',html);console.log('Built offline HTML:',Buffer.byteLength(html),'bytes');
