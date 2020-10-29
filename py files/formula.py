def point_tilt (x_pin,y_pin):
    # distance between f0 and pin
    x_f0p=float(x_f0-x_pin)
    y_f0p=float(y_f0-y_pin)
    hyp_f0p=float(math.sqrt((x_f0p*x_f0p)+(y_f0p*y_f0p)))
    #print "F0p", x_f0p, y_f0p, hyp_f0p

    # distance between f1 and pin
    x_f1p=float(x_f1-x_pin)
    y_f1p=float(y_f1-y_pin)
    hyp_f1p=float(math.sqrt((x_f1p*x_f1p)+(y_f1p*y_f1p)))
    #print "F1p", x_f1p, y_f1p, hyp_f1p

    # distance between f2 and pin
    x_f2p=float(x_f2-x_pin)
    y_f2p=float(y_f2-y_pin)
    hyp_f2p=float(math.sqrt((x_f2p*x_f2p)+(y_f2p*y_f2p)))
    #print "F2p", x_f2p, y_f2p, hyp_f2p

    # Sphere center of f0 with radius of hyp_f0p
    # Sphere center of f1 with radius of hyp_f1p
    # Sphere center of f2 with radius of hyp_f2p

    # Intersection between sphere_0p and sphere_1p creating circle01
    # Distance between spheres center
    d_1=x_t1-x_t0;
    d_2=y_t1-y_t0;
    d_3=z_t1-z_t0;
    d=math.sqrt(d_1*d_1 + d_2*d_2 + d_3*d_3);
    # Angle between sphere_0 center and intersection point
    top=float(hyp_f0p*hyp_f0p + d*d - hyp_f1p*hyp_f1p)
    bot=float(2*hyp_f0p*d)
    t=top/bot
    alpha=math.acos(t)
    # Intersection circle radius r_c_01
    r_c01=float(hyp_f0p*math.sin(alpha))
    # Plane intersection of S0p and S1p
    A1=float(2*d_1)
    B1=float(2*d_2)
    C1=float(2*d_3)
    D1=float(x_t0*x_t0 - x_t1*x_t1 + y_t0*y_t0 - y_t1*y_t1
             + z_t0*z_t0 - z_t1*z_t1 - hyp_f0p*hyp_f0p + hyp_f1p*hyp_f1p)
    top=float(x_t0*A1 + y_t0*B1 +z_t0*C1 + D1)
    bot=float(A1*(x_t0-x_t1) + B1*(y_t0-y_t1) + C1*(z_t0-z_t1))
    t=float(top/bot)
    x_c01=float(x_t0 + t*(x_t1 - x_t0))
    y_c01=float(y_t0 + t*(y_t1 - y_t0))
    z_c01=float(z_t0 + t*(z_t1 - z_t0))

    # Intersection between sphere_1p and sphere_2p creating circle12
    # Distance between spheres center
    d_1=x_t2-x_t1;
    d_2=y_t2-y_t1;
    d_3=z_t2-z_t1;
    d=math.sqrt(d_1*d_1 + d_2*d_2 + d_3*d_3);
    # Angle between sphere_1 center and intersection point
    top=float(hyp_f1p*hyp_f1p + d*d - hyp_f2p*hyp_f2p)
    bot=float(2*hyp_f1p*d)
    t=top/bot
    alpha=math.acos(t)
    # Intersection circle radius r_c_12
    r_c12=float(hyp_f1p*math.sin(alpha))
    # Plane intersection of S0p and S1p
    A2=float(2*d_1)
    B2=float(2*d_2)
    C2=float(2*d_3)
    D2=float(x_t1*x_t1 - x_t2*x_t2 + y_t1*y_t1 - y_t2*y_t2
             + z_t1*z_t1 - z_t2*z_t2 - hyp_f1p*hyp_f1p + hyp_f2p*hyp_f2p)
    top=float(x_t1*A2 + y_t1*B2 +z_t1*C2 + D2)
    bot=float(A2*(x_t1-x_t2) + B2*(y_t1-y_t2) + C2*(z_t1-z_t2))
    t=float(top/bot)
    x_c12=float(x_t1 + t*(x_t2 - x_t1))
    y_c12=float(y_t1 + t*(y_t2 - y_t1))
    z_c12=float(z_t1 + t*(z_t2 - z_t1))

    # Direction of line intersection between planes of circles
    # Set z=t
    x1=float((B2*D1-B1*D2)/(A2*B1-A1*B2))
    x2=float((B2*C1-B1*C2)/(A2*B1-A1*B2))
    y1=float((-D1/B1)-((A1/B1)*x1))
    y2=float(((A1/B1)*x2)+(C1/B1))
    z1=0
    z2=1

    # Intersection between line and sphere of circle01
    cgx=float(x_c01-x1)
    cgy=float(y_c01-y1)
    cgz=float(z_c01-z1)
    cg_sq=cgx*cgx + cgy*cgy + cgz*cgz

    gh_sq=math.fabs((r_c01*r_c01) - cg_sq)
    top=gh_sq
    a=x2*x2
    b=y2*y2
    c=z2*z2
    bot = a+b+c
    t_sq=float(top/bot)
    t=math.sqrt(t_sq)
    x_tilt=x1 + t*x2
    y_tilt=y1 - t*y2
