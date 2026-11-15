# מנגינת פתיחה קצרה (סולם "אהבה רבה"/פריגיש על רה) – פעמונים רכים + משטח מיתרים
import numpy as np, wave
SR=44100; D=6.2
t=np.arange(int(SR*D))/SR; out=np.zeros_like(t); outR=np.zeros_like(t)
def f(n): return 440*2**((n-69)/12)
def bell(st,midi,dur,amp,pan=0.0):
    i=int(st*SR); n=int(dur*SR); tt=np.arange(n)/SR
    fr=f(midi); s=np.zeros(n)
    for h,a,dc in [(1,1,2.2),(2,.35,3.5),(3,.12,5),(4.2,.05,7)]:
        s+=a*np.sin(2*np.pi*fr*h*tt)*np.exp(-dc*tt)
    s*=np.minimum(1,tt/0.008)*amp
    e=min(len(out),i+n); s=s[:e-i]
    out[i:e]+=s*(1-pan)*1.0; outR[i:e]+=s*(1+pan)*1.0
def pad(st,midis,dur,amp):
    i=int(st*SR); n=int(dur*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for m in midis:
        for det in (-0.12,0.12):
            fr=f(m+det); s+=np.sin(2*np.pi*fr*tt)+0.3*np.sin(2*np.pi*2*fr*tt)
    env=np.minimum(1,tt/1.2)*np.minimum(1,(dur-tt)/1.6).clip(0)
    s*=env*amp/len(midis)
    e=min(len(out),i+n); out[i:e]+=s[:e-i]; outR[i:e]+=s[:e-i]
# D=62 Eb=63 F#=66 G=67 A=69 Bb=70 C=72 D=74
mel=[(0.0,74,.9),(0.32,72,.7),(0.64,70,.7),(0.96,69,.8),(1.45,70,.6),(1.75,69,.6),(2.05,67,.6),(2.35,66,.9),(2.95,67,.7),(3.3,63,.8),(3.75,62,2.4)]
for k,(st,m,a) in enumerate(mel): bell(st,m,2.6,0.22*a,pan=(-.25 if k%2 else .25))
for st,m in [(0,50),(1.45,51),(2.35,50),(3.75,50)]: bell(st,m,2.4,0.16)
pad(0,[62,66,69],3.0,0.06); pad(2.2,[62,66,69,74],4.0,0.07)
# הד קל
dl=int(0.23*SR)
for ch in (out,outR):
    ch[dl:]+=0.28*ch[:-dl].copy()
fade=np.minimum(1,(D-t)/1.2).clip(0); out*=fade; outR*=fade
m=max(abs(out).max(),abs(outR).max()); L=out/m*0.8; R=outR/m*0.8
st=np.empty(2*len(t),dtype=np.int16); st[0::2]=(L*32767).astype(np.int16); st[1::2]=(R*32767).astype(np.int16)
w=wave.open('intro.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
