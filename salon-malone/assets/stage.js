/* Salon Malone — per-panel particle stages
   Each dark panel gets its own small WebGL stage. A stage holds one FORM
   (orb, rings, cone, galaxy, dust) and can assemble it from another form
   as the visitor scrolls into the panel — the morph is scoped to the scene
   it belongs to. Rendering is gated by visibility so four stages cost less
   than one always-on background. */
import * as THREE from 'three';

const rnd = (a=1,b)=> b===undefined ? Math.random()*a : a+Math.random()*(b-a);
const clamp = (v,a,b)=> v<a?a:v>b?b:v;
const smooth = t=> t*t*(3-2*t);

/* ---------- forms ---------- */
const FORMS = {
  dust(){ // the unworked list — scattered
    const u=Math.random()*Math.PI*2, c=rnd(-1,1), s=Math.sqrt(1-c*c), R=2.8+rnd(-0.7,1.4);
    return [Math.cos(u)*s*R, c*R*0.8, Math.sin(u)*s*R];
  },
  orb(){ // the voice — dense core, soft shell
    const u=Math.random()*Math.PI*2, c=rnd(-1,1), s=Math.sqrt(1-c*c);
    const R=1.18*(0.8+Math.pow(Math.random(),2.2)*0.32);
    return [Math.cos(u)*s*R, c*R, Math.sin(u)*s*R];
  },
  rings(){ // a turn on the line — concentric rings
    const k=(Math.random()*4)|0, r=0.55+k*0.47+rnd(-0.05,0.05), a=Math.random()*Math.PI*2;
    return [Math.cos(a)*r, rnd(-1,1)*0.05, Math.sin(a)*r];
  },
  cone(){ // the arithmetic — wide list, one chair
    const t=Math.pow(Math.random(),0.62), y=1.35-t*2.55, r=0.055+(1-t)*1.7;
    const a=Math.random()*Math.PI*2, j=0.045;
    return [Math.cos(a)*r+rnd(-j,j), y+rnd(-j,j), Math.sin(a)*r+rnd(-j,j)];
  },
  galaxy(){ // continuous work — a slow spiral
    const arm=(Math.random()*2)|0, t=Math.pow(Math.random(),0.9);
    const r=0.8+t*1.6, a=r*2.5+arm*Math.PI+rnd(-0.18,0.18);
    return [Math.cos(a)*r, rnd(-1,1)*0.045*(0.4+r*0.2), Math.sin(a)*r];
  },
};

const SAND=[0.914,0.780,0.608], ROSE=[0.851,0.627,0.706], WHITE=[0.92,0.94,0.97];

export function createStage(canvas, opts={}){
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const o = Object.assign({
    form:'orb', from:null, n: innerWidth<760 ? 5500 : 11000,
    camY:0.3, camZ:6.2, lookY:0, dim:1, spin:0.14, offX:0,
    pointer:false, halo:0.28, tiltX:0, size:21,
  }, opts);

  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true, powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio, innerWidth<760?1.5:2));
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);

  /* attributes: aA = entry form, aB = resting form */
  const N=o.n;
  const A=new Float32Array(N*3), B=new Float32Array(N*3);
  const col=new Float32Array(N*3), warm=new Float32Array(N*3);
  const siz=new Float32Array(N), seed=new Float32Array(N), spk=new Float32Array(N);
  const genA=FORMS[o.from||o.form], genB=FORMS[o.form];
  for(let i=0;i<N;i++){
    let p=genA(); A[i*3]=p[0];A[i*3+1]=p[1];A[i*3+2]=p[2];
    p=genB();     B[i*3]=p[0];B[i*3+1]=p[1];B[i*3+2]=p[2];
    const r=Math.random();
    const base=r<0.5?WHITE:r<0.84?SAND:ROSE, b=0.42+Math.random()*0.62;
    col[i*3]=base[0]*b; col[i*3+1]=base[1]*b; col[i*3+2]=base[2]*b;
    const wm=r<0.34?WHITE:r<0.8?SAND:ROSE;
    warm[i*3]=wm[0]*b*1.12; warm[i*3+1]=wm[1]*b*1.06; warm[i*3+2]=wm[2]*b*0.98;
    seed[i]=Math.random()*6.283; spk[i]=Math.random()<0.09?1:0;
    siz[i]=Math.random()<0.14?rnd(1.5,2.7):rnd(0.55,1.5);
  }
  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(B,3));
  geo.setAttribute('aA', new THREE.BufferAttribute(A,3));
  geo.setAttribute('aB', new THREE.BufferAttribute(B,3));
  geo.setAttribute('aColor', new THREE.BufferAttribute(col,3));
  geo.setAttribute('aWarm', new THREE.BufferAttribute(warm,3));
  geo.setAttribute('aSize', new THREE.BufferAttribute(siz,1));
  geo.setAttribute('aSeed', new THREE.BufferAttribute(seed,1));
  geo.setAttribute('aSpark', new THREE.BufferAttribute(spk,1));

  const mat=new THREE.ShaderMaterial({
    transparent:true, depthWrite:false, blending:THREE.AdditiveBlending,
    uniforms:{
      uTime:{value:0}, uSize:{value:renderer.getPixelRatio()*o.size},
      uMix:{value:o.from?0:1}, uDim:{value:o.dim}, uVoice:{value:0},
    },
    vertexShader:`
      uniform float uTime,uSize,uMix,uDim,uVoice;
      attribute vec3 aA,aB,aColor,aWarm; attribute float aSize,aSeed,aSpark;
      varying vec3 vColor; varying float vFade;
      void main(){
        vec3 p = mix(aA, aB, uMix);
        float d = length(p);
        float pulse = sin(d*3.4 - uTime*3.1 + aSeed*0.35);
        p *= 1.0 + uVoice*0.075*pulse;
        vec3 c = mix(aColor, aWarm, uVoice);
        float tw = 0.72 + 0.28*sin(uTime*1.7 + aSeed);
        float spark = aSpark*pow(0.5+0.5*sin(uTime*3.0 + aSeed*3.0), 8.0);
        vec4 mv = modelViewMatrix*vec4(p,1.0);
        float depth = -mv.z;
        float fade = smoothstep(8.4, 3.0, depth);
        vFade = fade;
        vColor = (c*(0.68+0.42*tw) + spark*1.35 + uVoice*0.10)*(0.40+0.60*fade)*uDim;
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

  /* soft halo */
  const gtex=(()=>{ const s=256,cv=document.createElement('canvas');cv.width=cv.height=s;
    const g=cv.getContext('2d'),rg=g.createRadialGradient(s/2,s/2,0,s/2,s/2,s/2);
    rg.addColorStop(0,'rgba(255,240,214,0.55)');rg.addColorStop(0.3,'rgba(233,199,155,0.16)');
    rg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=rg;g.fillRect(0,0,s,s);
    return new THREE.CanvasTexture(cv); })();
  const halo=new THREE.Sprite(new THREE.SpriteMaterial({map:gtex,color:0xE9C79B,transparent:true,
    opacity:o.halo,blending:THREE.AdditiveBlending,depthWrite:false}));
  halo.scale.set(5,5,1); halo.position.set(o.offX,0,-1.4); scene.add(halo);

  /* sizing to the canvas box */
  function size(){
    const w=canvas.clientWidth||2, h=canvas.clientHeight||2;
    renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix();
  }
  new ResizeObserver(size).observe(canvas); size();

  let visible=false, running=false, mix=o.from?0:1, tMix=o.from?0:1;
  let voice=0, tVoice=0, spin=0, px=0, py=0, tpx=0, tpy=0;
  const t0=performance.now();

  function frame(now){
    if(!visible){ running=false; return; }
    const t=(now-t0)/1000;
    mix += (tMix-mix)*0.10;
    voice += (tVoice-voice)*0.07;
    px += (tpx-px)*0.05; py += (tpy-py)*0.05;
    mat.uniforms.uTime.value=t;
    mat.uniforms.uMix.value=mix;
    mat.uniforms.uVoice.value=voice;
    halo.material.opacity=o.halo*(1+voice*0.5);
    spin += o.spin*0.016;
    points.rotation.y = spin + px*0.42;
    points.rotation.x = o.tiltX + Math.sin(t*0.28)*0.045 - py*0.3;
    points.position.x = o.offX * (innerWidth<1100?0:1);
    camera.position.set(px*0.25, o.camY, o.camZ);
    camera.lookAt(0, o.lookY, 0);
    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }
  function wake(){ if(visible && !running){ running=true; requestAnimationFrame(frame); } }

  if(o.pointer && !reduce){
    addEventListener('pointermove',e=>{ tpx=(e.clientX/innerWidth-0.5)*2; tpy=(e.clientY/innerHeight-0.5)*2; },{passive:true});
  }
  if(reduce){ mix=1; tMix=1; }

  return {
    setVisible(v){ visible=v; wake(); },
    setProgress(p){ if(!reduce && o.from) tMix=smooth(clamp(p*1.6,0,1)); },
    setVoice(v){ tVoice = reduce?0:(v?1:0); },
  };
}
