# print("Andromeda")
# andromeda = DSO.get(m="31")
# print(andromeda.angle)
# print(andromeda.maj_ax)
# print(andromeda.min_ax)

# HyperLEDA row:
# PGC0002557 J004244.3+411610 G  Sb    3.30+/-0.06  0.45+/-0.07   35.+/-  6.  5 NGC224                UGC454                MCG7-02-016           CGCG535-17            GIN801

# Can get magnitudes by querying for chunks of object names via:
# http://atlas.obs-hp.fr/hyperleda/fG.cgi?n=a107&c=o&of=1,leda,simbad&nra=l&sql=bandname%3D%27B%27&ob=&o=PGC2054947&a=html

# 3.30 = Apparent diameter from catalog
# x = 3.3
# D = 10**x
# D_arcmin = D * 0.1

# # L = Axis ratio in log scale (log of major axis to minor axis) -- this is from catalog directly
# L = 0.45
# R = 10**L

# b = D_arcmin / (2 * math.sqrt(R))
# a = D_arcmin * math.sqrt(R) / 2
# print("ab in arcmin")
# print(a, b)

# r = math.log(andromeda.maj_ax) / math.log(andromeda.min_ax)  # 1.22
# r = math.log(andromeda.maj_ax * 0.5 / andromeda.min_ax * 0.5)

# print(r)
# print("---")
