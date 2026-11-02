import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {createHash} from 'node:crypto';
test('forest-only revision preserves approved water, porcelain and narration',()=>{const expected={
 'dist/assets/audio/water-porcelain-bed-v043.mp3':'67e7f3288a553381a36392d4f9d171d0592c3e0d0fb3c1b2c2f275468d78a263',
 'dist/assets/audio/porcelain-soft-middle-v044.mp3':'a220f5d21f4405f1d6dce1db0457d3dadd4d61901f46db18cf4ca10a8cae778d',
 'dist/assets/audio/porcelain-soft-low-v044.mp3':'24acb8ad5ce2b9cde82a09a15477aad69f131de364b38e56fa7d588eb35af38a',
 'dist/assets/audio/porcelain-soft-high-v044.mp3':'09c1c5d4cd5e3edfb6ab4ce5e2a18a0b401772d0f3406d3bf262df877fc6b3d9',
 'dist/narration-assets.js':'13a1dbbc6faa50930cf920bb60a936d275cb193bc66e123ee37bd35858f70fd3'
};for(const [path,hash] of Object.entries(expected)){const bytes=fs.readFileSync(new URL('../'+path,import.meta.url));assert.equal(createHash('sha256').update(bytes).digest('hex'),hash,path);}});
