/* Carat Capital — cinematic particle engine
   A single Points system whose particles morph between three forms as the page
   scrolls: a brilliant-cut DIAMOND, a gold ORBITAL RING (the market in motion),
   and an ambient DUST field. Self-hosted three.js; additive glow; depth-faded
   for a true 3D read. Degrades to a calm static diamond under reduced-motion. */
import * as THREE from 'three';

export function initCinema(canvas){
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small  = innerWidth < 720;
  const N = small ? 9000 : 17000;

  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true, powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio, small?1.5:2));
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(36, 1, 0.1, 100);

  /* ---- vec helpers ---- */
  const rnd=(a=1,b)=> b===undefined?Math.random()*a:a+Math.random()*(b-a);
  const sub=(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]];
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const len=a=>Math.hypot(a[0],a[1],a[2]);
  const nrm=a=>{const l=len(a)||1;return[a[0]/l,a[1]/l,a[2]/l];};
  const lerp3=(a,b,t)=>[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t];
  const clamp=(v,a,b)=>v<a?a:v>b?b:v;
  const lerp=(a,b,t)=>a+(b-a)*t;
  const smooth=t=>t*t*(3-2*t);
  function ring(count,r,y,off=0){const a=[];for(let i=0;i<count;i++){const t=off+i/count*Math.PI*2;a.push([Math.cos(t)*r,y,Math.sin(t)*r]);}return a;}
  const normal=(p0,p1,p2)=>nrm(cross(sub(p1,p0),sub(p2,p0)));
  const triArea=(p0,p1,p2)=>0.5*len(cross(sub(p1,p0),sub(p2,p0)));

  /* ---- round brilliant model: facets + edges ---- */
  function diamondModel(){
    const Rt=0.55,Hc=0.46,Hp=1.0;
    const table=ring(8,Rt,Hc,Math.PI/8), g=ring(16,1,0,0);
    const culet=[0,-Hp,0], center=[0,Hc,0]; const F=[];
    for(let i=0;i<8;i++) F.push([center,table[i],table[(i+1)%8]]);
    for(let i=0;i<8;i++){const t0=table[i],t1=table[(i+1)%8];
      const g0=g[(2*i)%16],g1=g[(2*i+1)%16],g2=g[(2*i+2)%16];
      F.push([t0,g0,g1]);F.push([t0,g1,t1]);F.push([t1,g1,g2]);}
    for(let i=0;i<16;i++) F.push([g[i],g[(i+1)%16],culet]);
    const facets=F.map(([a,b,c])=>({p0:a,p1:b,p2:c,n:normal(a,b,c),area:triArea(a,b,c)}));
    const key=p=>p.map(v=>v.toFixed(4)).join(','); const em=new Map();
    for(const[a,b,c]of F)for(const[u,v]of[[a,b],[b,c],[c,a]]){const k=[key(u),key(v)].sort().join('|');if(!em.has(k))em.set(k,[u,v]);}
    const edges=[...em.values()].map(([u,v])=>({u,v,len:len(sub(v,u))}));
    return {facets,edges};
  }
  const galaxyPoint=()=>{const arm=(Math.random()*2)|0,t=Math.pow(Math.random(),.9),r=.85+t*1.5,
    ang=r*2.6+arm*Math.PI+rnd(-.16,.16),y=rnd(-1,1)*.035*(.4+r*.18);return[Math.cos(ang)*r,y,Math.sin(ang)*r];};

  /* ---- build attributes ---- */
  const {facets,edges}=diamondModel();
  const areaSum=facets.reduce((s,f)=>s+f.area,0);let acc=0;const fcum=facets.map(f=>(acc+=f.area,acc));
  let el=0;const ecum=edges.map(e=>(el+=e.len,el));const elen=el;
  const pickFacet=()=>{const x=Math.random()*areaSum;let lo=0,hi=fcum.length-1;while(lo<hi){const m=(lo+hi)>>1;fcum[m]<x?lo=m+1:hi=m;}return facets[lo];};
  const pickEdge=()=>{const x=Math.random()*elen;let lo=0,hi=ecum.length-1;while(lo<hi){const m=(lo+hi)>>1;ecum[m]<x?lo=m+1:hi=m;}return edges[lo];};

  const pos=new Float32Array(N*3),tg1=new Float32Array(N*3),tg2=new Float32Array(N*3);
  const col=new Float32Array(N*3),gcol=new Float32Array(N*3);
  const siz=new Float32Array(N),seed=new Float32Array(N),spk=new Float32Array(N);

  const cIvory=[0.80,0.88,0.98],cGold=[0.82,0.64,0.30],cGoldL=[0.96,0.84,0.52];
  const fire=[[0.20,1.0,0.60],[0.70,0.55,1.0],[0.95,0.35,0.18]];
  const L=nrm([0.35,0.9,0.45]);

  for(let i=0;i<N;i++){
    const roll=Math.random(); let p,n,isEdge=0;
    if(roll<0.60){const e=pickEdge(),t=Math.random();p=lerp3(e.u,e.v,t);const j=0.006;p=[p[0]+rnd(-j,j),p[1]+rnd(-j,j),p[2]+rnd(-j,j)];n=nrm(p);isEdge=1;}
    else{const f=pickFacet();let u=Math.random(),v=Math.random();if(u+v>1){u=1-u;v=1-v;}
      p=[f.p0[0]+u*(f.p1[0]-f.p0[0])+v*(f.p2[0]-f.p0[0]),f.p0[1]+u*(f.p1[1]-f.p0[1])+v*(f.p2[1]-f.p0[1]),f.p0[2]+u*(f.p1[2]-f.p0[2])+v*(f.p2[2]-f.p0[2])];n=f.n;
      if(roll>0.86){const d=0.05+Math.random()*0.14;p=[p[0]+f.n[0]*d,p[1]+f.n[1]*d,p[2]+f.n[2]*d];}}
    pos[i*3]=p[0];pos[i*3+1]=p[1];pos[i*3+2]=p[2];

    const d=Math.max(0,n[0]*L[0]+n[1]*L[1]+n[2]*L[2]),up=n[1],r2=Math.random();let c;
    if(isEdge){const b=0.6+d*0.5;c=r2<0.22?[cGoldL[0]*(0.7+d*0.5),cGoldL[1]*(0.7+d*0.5),cGoldL[2]*(0.7+d*0.5)]:[cIvory[0]*b,cIvory[1]*b,cIvory[2]*b];}
    else if(up>0.15&&r2<0.5){const b=0.35+d*0.7;c=[cIvory[0]*b,cIvory[1]*b,cIvory[2]*b];}
    else if(r2<0.68){const g0=r2<0.6?cGold:cGoldL,b=0.4+d*0.6;c=[g0[0]*b,g0[1]*b,g0[2]*b];}
    else if(r2<0.78){c=fire[(Math.random()*fire.length)|0].slice();}
    else{const b=0.22+d*0.4;c=[cIvory[0]*b,cIvory[1]*b,cIvory[2]*b];}
    col[i*3]=c[0];col[i*3+1]=c[1];col[i*3+2]=c[2];

    const gp=galaxyPoint();tg1[i*3]=gp[0];tg1[i*3+1]=gp[1];tg1[i*3+2]=gp[2];
    const rr=Math.hypot(gp[0],gp[2]),tc=Math.min(1,rr/2.2);
    gcol[i*3]=1.0*(1-tc)+0.65*tc;gcol[i*3+1]=0.78*(1-tc)+0.86*tc;gcol[i*3+2]=0.42*(1-tc)+1.0*tc;

    const uu=Math.random()*Math.PI*2,cph=rnd(-1,1),sph=Math.sqrt(1-cph*cph),R=2.8+rnd(-0.6,1.3);
    tg2[i*3]=Math.cos(uu)*sph*R;tg2[i*3+1]=cph*R*0.9;tg2[i*3+2]=Math.sin(uu)*sph*R;

    seed[i]=Math.random()*6.283; spk[i]=Math.random()<0.08?1:0;
    siz[i]=isEdge?rnd(0.7,1.5):(r2>0.78?rnd(1.0,2.0):rnd(0.5,1.1));
  }

  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  geo.setAttribute('aGalaxy',new THREE.BufferAttribute(tg1,3));
  geo.setAttribute('aDust',new THREE.BufferAttribute(tg2,3));
  geo.setAttribute('aColor',new THREE.BufferAttribute(col,3));
  geo.setAttribute('aGalCol',new THREE.BufferAttribute(gcol,3));
  geo.setAttribute('aSize',new THREE.BufferAttribute(siz,1));
  geo.setAttribute('aSeed',new THREE.BufferAttribute(seed,1));
  geo.setAttribute('aSpark',new THREE.BufferAttribute(spk,1));

  const mat=new THREE.ShaderMaterial({
    transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    uniforms:{uTime:{value:0},uSize:{value:renderer.getPixelRatio()*20},
      uWeights:{value:new THREE.Vector3(1,0,0)},uDim:{value:1}},
    vertexShader:`uniform float uTime,uSize,uDim;uniform vec3 uWeights;
      attribute vec3 aGalaxy,aDust,aColor,aGalCol;attribute float aSize,aSeed,aSpark;
      varying vec3 vColor;varying float vFade;
      void main(){
        vec3 p=position*uWeights.x+aGalaxy*uWeights.y+aDust*uWeights.z;
        vec3 c=aColor*(uWeights.x+uWeights.z)+aGalCol*uWeights.y;
        float tw=0.7+0.3*sin(uTime*1.8+aSeed);
        float spark=aSpark*pow(0.5+0.5*sin(uTime*3.2+aSeed*3.0),8.0);
        vec4 mv=modelViewMatrix*vec4(p,1.0);float depth=-mv.z;
        float fade=smoothstep(7.8,3.4,depth);vFade=fade;
        vColor=(c*(0.7+0.35*tw)+spark*1.5)*(0.42+0.58*fade)*uDim;
        gl_PointSize=aSize*(1.0+spark*1.4)*uSize/depth;
        gl_Position=projectionMatrix*mv;
      }`,
    fragmentShader:`varying vec3 vColor;varying float vFade;
      void main(){vec2 d=gl_PointCoord-0.5;float r=dot(d,d);
        float a=smoothstep(0.25,0.0,r),core=smoothstep(0.04,0.0,r);
        gl_FragColor=vec4(vColor+core*0.5,a*(0.55+0.45*vFade));}`
  });
  const points=new THREE.Points(geo,mat); scene.add(points);

  /* soft halo */
  function makeGlow(){const s=256,cv=document.createElement('canvas');cv.width=cv.height=s;const g=cv.getContext('2d');
    const rg=g.createRadialGradient(s/2,s/2,0,s/2,s/2,s/2);
    rg.addColorStop(0,'rgba(255,238,196,0.55)');rg.addColorStop(0.3,'rgba(206,166,86,0.18)');rg.addColorStop(1,'rgba(0,0,0,0)');
    g.fillStyle=rg;g.fillRect(0,0,s,s);return new THREE.CanvasTexture(cv);}
  const halo=new THREE.Sprite(new THREE.SpriteMaterial({map:makeGlow(),color:0xC6A24A,transparent:true,opacity:0.30,blending:THREE.AdditiveBlending,depthWrite:false}));
  halo.scale.set(4.6,4.6,1); scene.add(halo);

  /* ---- scroll scheduling ---- */
  // keyframes: progress -> [wDiamond,wGalaxy,wDust, camY, camZ, lookY, haloOp, dim, spin]
  // Bright feature shapes at hero (small high diamond) and motion (centred galaxy);
  // a dim atmospheric field everywhere else so editorial text stays legible.
  const KF=[
    [0.00, 1,0,0,    1.05,7.6,-1.02, 0.26,1.00, 0.22],
    [0.06, 1,0,0,    1.05,7.6,-1.02, 0.26,1.00, 0.22],
    [0.17, 1,0,0,    0.92,5.7,-0.14, 0.40,0.95, 0.26],
    [0.28, 0,1,0,    0.72,5.4, 0.00, 0.30,1.00, 0.30],
    [0.44, 0,1,0,    0.55,5.6, 0.05, 0.22,0.46, 0.18],
    [0.56, 0,0.35,0.65, 0.40,6.0, 0.00, 0.16,0.40, 0.12],
    [0.66, 0,0,1,    0.28,6.3, 0.00, 0.12,0.40, 0.10],
    [0.74, 0,0,1,    0.28,6.3, 0.00, 0.08,0.16, 0.08],
    [0.84, 0,0,1,    0.35,6.0,-0.05, 0.16,0.55, 0.10],
    [0.90, 0.5,0,0.5,0.55,5.6,-0.15, 0.26,0.60, 0.18],
    [0.99, 0,0,1,    0.70,5.6,-0.10, 0.34,0.72, 0.16],
    [1.00, 0,0,1,    0.70,5.6,-0.10, 0.34,0.72, 0.16],
  ];
  function sample(g){
    g=clamp(g,0,1); let a=KF[0],b=KF[KF.length-1];
    for(let i=0;i<KF.length-1;i++){if(g>=KF[i][0]&&g<=KF[i+1][0]){a=KF[i];b=KF[i+1];break;}}
    const span=(b[0]-a[0])||1; const t=smooth(clamp((g-a[0])/span,0,1));
    const o=[];for(let k=1;k<a.length;k++)o.push(lerp(a[k],b[k],t));return o;
  }

  let progress=0, targetProgress=0, px=0, py=0, tpx=0, tpy=0;
  const state={dw:1,gw:0,uw:0};

  function resize(){const w=innerWidth,h=innerHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
  addEventListener('resize',resize); resize();

  let t0=performance.now(), spin=0;
  function frame(now){
    const t=(now-t0)/1000;
    progress += (targetProgress-progress)*0.11;   // eased follow
    px += (tpx-px)*0.05; py += (tpy-py)*0.05;
    const [dw,gw,uw,camY,camZ,lookY,haloOp,dim,sp]=sample(progress);
    mat.uniforms.uTime.value=t;
    mat.uniforms.uWeights.value.set(dw,gw,uw);
    mat.uniforms.uDim.value=dim;
    halo.material.opacity=haloOp;
    spin += sp*0.016;
    points.rotation.y = spin + px*0.5;
    points.rotation.x = Math.sin(t*0.3)*0.05 - 0.04 - py*0.35 + gw*0.05;
    halo.position.set(0, lookY, -1.2);
    camera.position.set(px*0.3, camY, camZ);
    camera.lookAt(0, lookY, 0);
    renderer.render(scene,camera);
    if(!reduce) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  if(reduce){ // one calm frame, no morph
    targetProgress=0; progress=0;
    const loop=(now)=>{const t=(now-t0)/1000;mat.uniforms.uTime.value=t;points.rotation.y=t*0.12;renderer.render(scene,camera);requestAnimationFrame(loop);};
    requestAnimationFrame(loop);
  }

  return {
    setProgress(g){ targetProgress = reduce?0:clamp(g,0,1); },
    setPointer(x,y){ tpx=x; tpy=y; },
    resize
  };
}
