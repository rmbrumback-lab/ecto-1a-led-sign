// Independent check: decode our .jt with JT-Edit's own import function.
// JT-Edit (GPL-3.0, https://github.com/auc0le/JT-Edit) is NOT included here; clone it yourself.
//
//   git clone https://github.com/auc0le/JT-Edit.git
//   node tools/verify_with_jtedit.js ./JT-Edit dist/Ecto-1A_GB2_16x96.jt
//
// Prints frame count/size and a few rows of frame 0 using JT-Edit's colour names.
const fs = require('fs');
const path = require('path');
const [jtEditDir, jtFile] = process.argv.slice(2);
if (!jtEditDir || !jtFile) { console.error('usage: node verify_with_jtedit.js <JT-Edit dir> <file.jt>'); process.exit(2); }

const src = fs.readFileSync(path.join(jtEditDir, 'app.js'), 'utf8');
const start = src.indexOf('function convertToPixelArrayFrames(');
const end = src.indexOf('}', src.indexOf('\nreturn pixelArrayFrames', start)) + 1;
const pb = src.indexOf('function putBinaryComponent');
const pbEnd = src.indexOf('}', src.indexOf('return colorMap', pb)) + 1;
if (start < 0 || pb < 0) { console.error('JT-Edit layout changed; decoder not found'); process.exit(1); }

global.document = { getElementById: () => ({ value: '' }) };
eval(src.slice(start, end) + '\nfunction bitshft(i,n){return (i>>n)&1;}\n' + src.slice(pb, pbEnd) +
     '\nglobal.decode = convertToPixelArrayFrames;');

const d = JSON.parse(fs.readFileSync(jtFile))[0].data;
const frames = decode(d.aniData || d.graffitiData, d.pixelWidth, d.pixelHeight, d.frameNum || 1);
const sym = { '#000000': ' ', '#FF0000': 'R', '#00FF00': 'G', '#FFFF00': 'Y' };
let unknown = 0;
frames.forEach(f => f.forEach(r => r.forEach(c => { if (!(c in sym)) unknown++; })));
console.log(`JT-Edit decoded ${frames.length} frames of ${frames[0].length}x${frames[0][0].length}; ` +
            `non-red/green/yellow pixels: ${unknown}`);
frames[0].forEach(r => console.log('|' + r.map(c => sym[c] || '?').join('') + '|'));
process.exit(unknown ? 1 : 0);
