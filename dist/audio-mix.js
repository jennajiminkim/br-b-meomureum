/** Bounded intervals in session seconds. Preview deliberately guarantees one representative event. */
export const AUDIO_MIX={
 water:{first:[1.8,3.5],interval:[4.8,10.5],accentGain:.5,gainRange:[.86,1.04],pan:.28},
 forest:{first:[12,24],interval:[32,68],accentGain:.6825,pan:.28}
};
export function nextAccentDelay(world,initial=false,random=Math.random){const [min,max]=AUDIO_MIX[world][initial?'first':'interval'];return min+random()*(max-min);}
