_A=' '
import math,random
class Erreur:
	def __init__(B,message):A=message;print('Erreur log : '+A);B.message=A
	def __str__(A):return'ERR: '+A.message
class Intervalle_net_continu:
	def __init__(A,a1,a2):A.a1=a1;A.a2=a2
	def __str__(A):return'['+str(A.a1)+', '+str(A.a2)+']'
	def __add__(A,other):B=other;return Intervalle_net(A.a1+B.a1,A.a2+B.a2)
	def __neg__(A):return Intervalle_net(-A.a2,-A.a1)
	def __sub__(A,other):return A+-other
	def __mul__(A,other):B=other;return Intervalle_net(max([A.a1*B.b1,A.a1*B.b2,A.a2*B.b1,A.a2*B.b2]),max([A.b1*B.a1,A.b1*B.a2,A.b2*B.a1,A.b2*B.a2]))
	def __pow__(A,value):
		if value!=-1:return Erreur('Only -1 is supported')
		if A.a1==0 or A.a2==0:return Erreur('Only non-zero intervals are supported')
		if A.a1<=0<=A.a2:return Erreur('Only  strictly positive or strictly négative intervals are supported by this operation.')
		return Intervalle_net(1/A.a2,1/A.a1)
	def __div__(A,other):return A*other**-1
	def union(A,other):
		B=other
		if A.a2<B.a1 or B.a2<A.a1:return Erreur('The intervals must be joined')
		return Intervalle_net(min(A.a1,B.a1),max(A.a2,B.a2))
	def __str__(A):return'['+str(A.a1)+';'+str(A.a2)+']'
class Intervalle_net:
	def __init__(C,*A):
		if len(A)%2!=0:0
		C.intervalles_continus=[]
		for B in range(0,len(A),2):
			if A[B]>=A[B+1]:return Erreur('The arguments must be ordered')
			C.intervalles_continus.append(Intervalle_net_continu(A[B],A[B+1]))
	def simplifier(A):
		for B in range(len(A.intervalles_continus)):
			for C in range(B+1,len(A.intervalles_continus)):
				if A.intervalles_continus[B].a2>=A.intervalles_continus[C].a1:A.intervalles_continus[B]=A.intervalles_continus[B]+A.intervalles_continus[C];del A.intervalles_continus[C];break
	def __str__(A):return str(A.intervalles_continus)
class UnionIFT:
	def __init__(A,IFTS,Tco=max):A.IFTS=IFTS;A.Tco=Tco
	def possibilite(C,other):
		B=other;A=0
		if isinstance(B,UnionIFT):
			for D in C.IFTS:A=max(A,D.possibilite(B))
			return A
		for E in C.IFTS:A=max(A,E.possibilite(B))
		return A
	def valeur(B,x):
		A=0
		for C in B.IFTS:A=B.Tco(C.valeur(x),A)
		return A
	def alpha_coupe(B,alpha):
		A=[A.alpha_coupe(alpha)for A in B.IFTS if A.alpha_coupe!=None];A=[(A.a1,A.a2)for A in A]
		if len(A)>0:C,D=min([A[0]for A in A]),max([A[1]for A in A]);return Intervalle_net_continu(C,D)
		else:return
class InterIFT:
	def __init__(A,IFTS,Tno=min):A.IFTS=IFTS;A.Tno=Tno
	def valeur(B,x):
		A=1
		for C in B.IFTS:A=B.Tno(C.valeur(x),A)
		return A
	def alpha_coupe(B,alpha):
		A=[A.alpha_coupe(alpha)for A in B.IFTS if A.alpha_coupe!=None];A=[(A.a1,A.a2)for A in A]
		if len(A)>0:C,D=max([A[0]for A in A]),min([A[1]for A in A]);return Intervalle_net_continu(C,D)
		else:return
def line(p1,p2):B=p2;A=p1;C=A[1]-B[1];D=B[0]-A[0];E=A[0]*B[1]-B[0]*A[1];F,G=A;H,I=B;return C,D,-E,F,G,H,I
def intersection(L1,L2):
	B=L2;A=L1;C=A[0]*B[1]-A[1]*B[0];I=A[2]*B[1]-A[1]*B[2];J=A[0]*B[2]-A[2]*B[0];E,N,F,O=A[3:];G,P,H,Q=B[3:];K=max(min(E,F),min(G,H));L=min(max(E,F),max(G,H))
	if C!=0:
		D=I/C;M=J/C
		if D<K or D>L:return
		return D,M
	else:return
class Trapeseflou:
	def __init__(A,a1,a2,a3,a4,h=1):
		if not a1<=a2<=a3<=a4:0
		A.a1=a1;A.a2=a2;A.a3=a3;A.a4=a4;A.h=h;A.lines=[line((A.a1,0),(A.a2,A.h)),line((A.a2,A.h),(A.a3,A.h)),line((A.a3,A.h),(A.a4,0))]
	def possibilite(B,other):
		A=other
		if isinstance(A,UnionIFT):return A.possibilite(B)
		C=[]
		for E in B.lines:
			for F in A.lines:
				D=intersection(E,F)
				if D!=None:C.append(D)
		if len(C)==0:
			if B.a1>=A.a1 and B.a4<=A.a4 or A.a1>=B.a1 and A.a4<=B.a4:return min(B.h,A.h)
			return 0
		return max([A[1]for A in C])
	def __add__(C,other):
		A=other
		if C.h>A.h:B=C.troncature(A.h)
		else:B=C;A=A.troncature(C.h)
		return Trapeseflou(B.a1+A.a1,B.a2+A.a2,B.a3+A.a3,B.a4+A.a4,B.h)
	def __mul__(A,other):
		E=other
		if isinstance(E,Trapeseflou):
			C=E
			if A.h>C.h:D=A.troncature(C.h)
			else:D=A;C=C.troncature(A.h)
			return Trapeseflou(D.a1*C.a1,D.a2*C.a2,D.a3*C.a3,D.a4*C.a4,D.h)
		else:
			B=E
			if B>0:F=B*A.a1;G=B*A.a2;H=B*A.a3;I=B*A.a4
			else:F=B*A.a4;G=B*A.a3;H=B*A.a2;I=B*A.a1
			return Trapeseflou(F,G,H,I,A.h)
	def __pow__(A,value):
		B=value
		if B==-1:return Trapeseflou(1/A.a4,1/A.a3,1/A.a2,1/A.a1,A.h)
		elif B==1:return A
		else:return A*A**(B-1)
	def __truediv__(A,other):return A*other**-1
	def __neg__(A):return Trapeseflou(-A.a4,-A.a3,-A.a2,-A.a1,A.h)
	def __sub__(A,other):return A+-other
	def troncature(A,h):
		if type(h)!=float and type(h)!=int:return Erreur(str(h)+' not int or float')
		if h>A.h:return Erreur(str(h)+"> h de l'intervalle")
		elif h==A.h:return A
		else:B=h*(A.a2-A.a1)/A.h+A.a1;C=-h*(A.a4-A.a3)/A.h+A.a4;return Trapeseflou(A.a1,B,C,A.a4,h)
	def valeur(A,x):
		if x==A.a2:return A.h
		if x<=A.a1:return 0
		if A.a1<x<=A.a2:return A.h*((x-A.a1)/(A.a2-A.a1))
		if A.a2<x<=A.a3:return A.h
		if A.a3<x<=A.a4:return A.h*((A.a4-x)/(A.a4-A.a3))
		if x>A.a4:return 0
	def alpha_coupe(A,alpha):
		B=alpha
		if B>0 and B<=A.h:C=(A.a2-A.a1)*(B/A.h)+A.a1;D=-(A.a4-A.a3)*(B/A.h)+A.a4;return Intervalle_net_continu(C,D)
		else:return
	def __str__(A):
		if A.a2==A.a3:return'NFT['+str(A.a1)+_A+str(A.a2)+_A+str(A.a3)+_A+'h='+str(A.h)+']'
		return'IFT['+str(A.a1)+_A+str(A.a2)+_A+str(A.a3)+_A+str(A.a4)+' h='+str(A.h)+']'
def convert_to_float(nombre):
	D=' not float';A=nombre;print(A)
	if','in A or'.'in A:
		B=A.replace(',','.')
		try:C=float(B)
		except:return Erreur(str(A)+D)
		return float(B)
	try:C=int(A)
	except:return Erreur(str(A)+D)
	return C
def parseIFT(chaine):
	A=[convert_to_float(A)for A in chaine.split(_A)if len(A)>0]
	if any(type(A)==Erreur for A in A):return A.index(key=lambda x:type(x)==Erreur)
	B=len(A)
	if any([C<A[B]for(B,C)in enumerate(A[1:])]):return Erreur('Bornes mal ordonnées')
	match B:
		case 2:return Intervalle_net_continu(A[0],A[1])
		case 3:return Trapeseflou(A[0],A[1],A[1],A[2])
		case 4:
			if 0<A[3]<1:return Trapeseflou(A[0],A[1],A[1],A[2],h=A[3])
			else:return Trapeseflou(A[0],A[1],A[2],A[3])
		case 5:return Trapeseflou(A[0],A[1],A[2],A[3],h=A[4])
	return Erreur('Pas le bon nombre de paramètres')
def check_erreur(a,b):
	if isinstance(a,Erreur):return a
	elif isinstance(b,Erreur):return b
def mul(a,b):
	if(A:=check_erreur(a,b)):return A
	return mul(a,b)
def add(a,b):
	if(A:=check_erreur(a,b)):return A
	return a+b
def sub(a,b):
	if(A:=check_erreur(a,b)):return A
	return a.__sub__(b)
def div(a,b):
	if(A:=check_erreur(a,b)):return A
	return a.__truediv__(b)
def tronc(a,b):
	if(A:=check_erreur(a,b)):return A
	return a.troncature(b)
def isnumeric(chaine):
	try:float(chaine);return True
	except:return False