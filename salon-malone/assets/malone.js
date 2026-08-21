/* Salon Malone — cinematic particle engine
   One Points system whose particles morph between five forms as the page
   scrolls, each one meaning something in the story:

     DUST    the dead client list — cold, scattered, going nowhere
     ORB     the concierge voice waking up
     RINGS   a turn on the line — concentric voice rings
     CONE    the arithmetic — 1,200 names funnelling down to 25 chairs
     GALAXY  where this goes — the marketing harness, working continuously

   Self-hosted three.js, additive glow, depth-faded for a real 3D read.
   Degrades to a calm breathing orb under prefers-reduced-motion. */
import * as THREE from 'three';

export function initMalone(canvas){
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small  = innerWidth < 760;
  const N = small ? 9000 : 18000;

  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true, powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio, small?1.5:2));
  renderer.setClearColor(0x000000, 0);
  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);

  /* ---------- helpers ---------- */
  const rnd=(a=1,b)=> b===undefined?Math.random()*a:a+Math.random()*(b-a);
  const clamp=(v,a,b)=>v<a?a:v>b?b:v;
  const lerp=(a,b,t)=>a+(b-a)*t;
  const smooth=t=>t*t*(3-2*t);

  /* ---------- the five forms ---------- */
  // scattered, drifting, unloved
  const dust=()=>{
    const u=Math.random()*Math.PI*2, c=rnd(-1,1), s=Math.sqrt(1-c*c), R=2.9+rnd(-0.7,1.5);
    return [Math.cos(u)*s*R, c*R*0.82, Math.sin(u)*s*R];
  };
  // a voice: dense core, soft shell
  const orb=()=>{
    const u=Math.random()*Math.PI*2, c=rnd(-1,1), s=Math.sqrt(1-c*c);
    const R=1.16*(0.82+Math.pow(Math.random(),2.1)*0.30);
    return [Math.cos(u)*s*R, c*R, Math.sin(u)*s*R];
  };
  // a turn on the line: concentric rings radiating out
  const rings=()=>{
    const k=(Math.random()*4)|0;                 // which ring
    const r=0.55+k*0.46+rnd(-0.05,0.05);
    const a=Math.random()*Math.PI*2;
    return [Math.cos(a)*r, rnd(-1,1)*0.055, Math.sin(a)*r];
  };
  // the funnel: wide at the top, one chair at the bottom
  const cone=()=>{
    const t=Math.pow(Math.random(),0.62);        // more mass up top
    const y=1.35-t*2.55;
    const r=0.055+(1-t)*1.72;
    const a=Math.random()*Math.PI*2;
    const j=0.045;
    return [Math.cos(a)*r+rnd(-j,j), y+rnd(-j,j), Math.sin(a)*r+rnd(-j,j)];
  };
  // continuous work: a slow two-arm spiral
  const galaxy=()=>{
    const arm=(Math.random()*2)|0, t=Math.pow(Math.random(),0.9);
    const r=0.8+t*1.6, a=r*2.5+arm*Math.PI+rnd(-0.18,0.18);
    return [Math.cos(a)*r, rnd(-1,1)*0.045*(0.4+r*0.2), Math.sin(a)*r];
  };

  /* ---------- attributes ---------- */
  const A={dust:new Float32Array(N*3), orb:new Float32Array(N*3), rings:new Float32Array(N*3),
           cone:new Float32Array(N*3), gal:new Float32Array(N*3)};
  const col=new Float32Array(N*3), warm=new Float32Array(N*3);
  const siz=new Float32Array(N), seed=new Float32Array(N), spk=new Float32Array(N);

  // brand palette, linearised for additive light
  const SAND=[0.914,0.780,0.608], ROSE=[0.851,0.627,0.706], WHITE=[0.92,0.94,0.97];

  for(let i=0;i<N;i++){
    const put=(arr,p)=>{arr[i*3]=p[0];arr[i*3+1]=p[1];arr[i*3+2]=p[2];};
    put(A.dust,dust()); put(A.orb,orb()); put(A.rings,rings()); put(A.cone,cone()); put(A.gal,galaxy());

    const r=Math.random();
    const base = r<0.50 ? WHITE : r<0.84 ? SAND : ROSE;
    const b = 0.42+Math.random()*0.62;
    col[i*3]=base[0]*b; col[i*3+1]=base[1]*b; col[i*3+2]=base[2]*b;
    // warm variant used when the voice is "speaking"
    const wm = r<0.34 ? WHITE : r<0.80 ? SAND : ROSE;
    warm[i*3]=wm[0]*(b*1.12); warm[i*3+1]=wm[1]*(b*1.06); warm[i*3+2]=wm[2]*(b*0.98);

    seed[i]=Math.random()*6.283;
    spk[i]=Math.random()<0.09?1:0;
    siz[i]=Math.random()<0.14?rnd(1.5,2.7):rnd(0.55,1.5);
  }

  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(A.orb,3));   // start on the orb
  geo.setAttribute('aDust',  new THREE.BufferAttribute(A.dust,3));
  geo.setAttribute('aOrb',   new THREE.BufferAttribute(A.orb,3));
  geo.setAttribute('aRings', new THREE.BufferAttribute(A.rings,3));
  geo.setAttribute('aCone',  new THREE.BufferAttribute(A.cone,3));
  geo.setAttribute('aGal',   new THREE.BufferAttribute(A.gal,3));
  geo.setAttribute('aColor', new THREE.BufferAttribute(col,3));
  geo.setAttribute('aWarm',  new THREE.BufferAttribute(warm,3));
  geo.setAttribute('aSize',  new THREE.BufferAttribute(siz,1));
  geo.setAttribute('aSeed',  new THREE.BufferAttribute(seed,1));
  geo.setAttribute('aSpark', new THREE.BufferAttribute(spk,1));

  const mat=new THREE.ShaderMaterial({
    transparent:true, depthWrite:false, blending:THREE.AdditiveBlending,
    uniforms:{
      uTime:{value:0}, uSize:{value:renderer.getPixelRatio()*22},
      uW:{value:new Float32Array([0,1,0,0,0])},   // dust, orb, rings, cone, galaxy
      uDim:{value:1}, uVoice:{value:0},           // uVoice: 0..1 speaking pulse
    },
    vertexShader:`
      uniform float uTime,uSize,uDim,uVoice; uniform float uW[5];
      attribute vec3 aDust,aOrb,aRings,aCone,aGal,aColor,aWarm;
      attribute float aSize,aSeed,aSpark;
      varying vec3 vColor; varying float vFade;
      void main(){
        vec3 p = aDust*uW[0] + aOrb*uW[1] + aRings*uW[2] + aCone*uW[3] + aGal*uW[4];

        // the voice breathes: a radial pulse travelling outward while speaking
        float d = length(p);
        float pulse = sin(d*3.4 - uTime*3.1 + aSeed*0.35);
        p *= 1.0 + uVoice * 0.075 * pulse;

        vec3 c = mix(aColor, aWarm, uVoice);
        float tw = 0.72 + 0.28*sin(uTime*1.7 + aSeed);
        float spark = aSpark*pow(0.5+0.5*sin(uTime*3.0 + aSeed*3.0), 8.0);

        vec4 mv = modelViewMatrix*vec4(p,1.0);
        float depth = -mv.z;
        float fade = smoothstep(8.4, 3.0, depth);
        vFade = fade;
        vColor = (c*(0.68+0.42*tw) + spark*1.35 + uVoice*0.10) * (0.40+0.60*fade) * uDim;

        gl_PointSize = aSize*(1.0+spark*1.5)*uSize/depth;
        gl_Position = projectionMatrix*mv;
      }`,
    fragmentShader:`
      varying vec3 vColor; varying float vFade;
      void main(){
        vec2 d=gl_PointCoord-0.5; float r=dot(d,d);
        float a=smoothstep(0.25,0.0,r), core=smoothstep(0.035,0.0,r);
        gl_FragColor=vec4(vColor+core*0.45, a*(0.55+0.45*vFade));
      }`
  });
  const points=new THREE.Points(geo,mat); scene.add(points);

  /* soft halo behind the form */
  function glowTex(){
    const s=256, cv=document.createElement('canvas'); cv.width=cv.height=s;
    const g=cv.getContext('2d'), rg=g.createRadialGradient(s/2,s/2,0,s/2,s/2,s/2);
    rg.addColorStop(0,'rgba(255,240,214,0.55)'); rg.addColorStop(0.3,'rgba(233,199,155,0.16)');
    rg.addColorStop(1,'rgba(0,0,0,0)'); g.fillStyle=rg; g.fillRect(0,0,s,s);
    return new THREE.CanvasTexture(cv);
  }
  const halo=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex(),color:0xE9C79B,transparent:true,
    opacity:0.3,blending:THREE.AdditiveBlending,depthWrite:false}));
  halo.scale.set(5.2,5.2,1); scene.add(halo);

  /* ---------- scenes ----------
     phase -> [dust,orb,rings,cone,galaxy, camY,camZ,lookY, halo, dim, spin, offX] */
  const KF=[
    [0.00, 1,0,0,0,0,  0.30,7.4, 0.00, 0.16,0.62, 0.05,  0.00],  // list, scattered
    [0.08, 0,1,0,0,0,  0.30,7.0, 0.00, 0.30,0.88, 0.12,  0.00],  // hero: the voice
    [0.20, 0,0,1,0,0,  0.86,7.2, 0.00, 0.20,0.44, 0.16,  0.00],  // the call: voice rings
    [0.32, 0,0,1,0,0,  1.35,6.8, 0.00, 0.12,0.26, 0.12,  0.00],  // science, behind text
    [0.44, 0,0.35,0,0,0.65, 1.05,6.6, 0.00, 0.10,0.20, 0.08,  0.00], // method, quiet
    [0.56, 0,1,0,0,0,  0.26,6.6, 0.00, 0.24,0.62, 0.12,  0.00],  // guardrail statement
    [0.68, 0,0,0,1,0,  0.05,6.4,-0.05, 0.16,0.90, 0.10,  2.05],  // the arithmetic funnel
    [0.78, 0,0,0,0,1,  0.80,6.0, 0.00, 0.20,0.60, 0.20, -1.45],  // thesis / future
    [0.88, 0,0,0,0,1,  0.45,6.2, 0.00, 0.12,0.26, 0.12,  0.00],  // pricing, quiet
    [0.96, 0,1,0,0,0,  0.28,6.8, 0.00, 0.20,0.40, 0.10,  1.30],  // faq / close
    [1.00, 0,1,0,0,0,  0.28,6.8, 0.00, 0.20,0.40, 0.10,  1.30],
  ];
  function sample(g){
    g=clamp(g,0,1); let a=KF[0], b=KF[KF.length-1];
    for(let i=0;i<KF.length-1;i++){ if(g>=KF[i][0]&&g<=KF[i+1][0]){a=KF[i];b=KF[i+1];break;} }
    const t=smooth(clamp((g-a[0])/((b[0]-a[0])||1),0,1));
    const o=[]; for(let k=1;k<a.length;k++) o.push(lerp(a[k],b[k],t));
    return o;
  }

  let progress=0, target=0, px=0, py=0, tpx=0, tpy=0, voice=0, tVoice=0, spin=0;

  function resize(){
    const w=innerWidth, h=innerHeight;
    renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix();
  }
  addEventListener('resize', resize); resize();

  const t0=performance.now();
  function frame(now){
    const t=(now-t0)/1000;
    progress += (target-progress)*0.10;
    px += (tpx-px)*0.05; py += (tpy-py)*0.05;
    voice += (tVoice-voice)*0.07;

    const [wD,wO,wR,wC,wG, camY,camZ,lookY, haloOp, dim, sp, offX] = sample(progress);
    mat.uniforms.uTime.value=t;
    mat.uniforms.uW.value[0]=wD; mat.uniforms.uW.value[1]=wO; mat.uniforms.uW.value[2]=wR;
    mat.uniforms.uW.value[3]=wC; mat.uniforms.uW.value[4]=wG;
    mat.uniforms.uDim.value = dim * (innerWidth<1100 ? 0.62 : 1);
    mat.uniforms.uVoice.value=voice;
    halo.material.opacity=haloOp*(1+voice*0.45);

    spin += sp*0.016;
    points.rotation.y = spin + px*0.42;
    points.rotation.x = Math.sin(t*0.28)*0.045 - py*0.30;
    const ox = offX * (innerWidth<1100 ? 0 : 1);
    points.position.x = ox;
    halo.position.set(ox, lookY, -1.4);
    camera.position.set(px*0.26, camY, camZ);
    camera.lookAt(0, lookY, 0);
    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  if(reduce){ target=0.08; progress=0.08; }   // hold on the calm orb

  return {
    setProgress(g){ if(!reduce) target=clamp(g,0,1); },
    setPointer(x,y){ if(!reduce){ tpx=x; tpy=y; } },
    speak(on){ tVoice = (reduce||!on) ? 0 : 1; },
    resize
  };
}
