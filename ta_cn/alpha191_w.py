"""alpha191的实现"""
from .imports_gtja_w import *


def alpha_001(OPEN, CLOSE, VOLUME, **kwargs):
    """Alpha1 (-1 * CORR(RANK(DELTA(LOG(VOLUME), 1)), RANK(((CLOSE - OPEN) / OPEN)), 6))"""
    return (-1 * CORR(RANK(DELTA(LOG(VOLUME), 1)), RANK(((CLOSE - OPEN) / OPEN)), 6))


def alpha_002(HIGH, LOW, CLOSE, **kwargs):
    """Alpha2 (-1 * DELTA((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)), 1))"""
    return (-1 * DELTA((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)), 1))


def alpha_003(HIGH, LOW, CLOSE, **kwargs):
    """Alpha3 SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),6)"""
    t1 = MAX(HIGH, DELAY(CLOSE, 1))
    t2 = MIN(LOW, DELAY(CLOSE, 1))
    t3 = IF(CLOSE > DELAY(CLOSE, 1), t2, t1)
    t4 = IF(CLOSE == DELAY(CLOSE, 1), 0, CLOSE - t3)
    return SUM(t4, 6)


def alpha_004(CLOSE, VOLUME, **kwargs):
    """Alpha4 ((((SUM(CLOSE, 8) / 8) + STD(CLOSE, 8)) < (SUM(CLOSE, 2) / 2)) ? (-1 * 1) : (((SUM(CLOSE, 2) / 2) <
((SUM(CLOSE, 8) / 8) - STD(CLOSE, 8))) ? 1 : (((1 < (VOLUME / MEAN(VOLUME,20))) || ((VOLUME /
MEAN(VOLUME,20)) == 1)) ? 1 : (-1 * 1))))"""
    x1 = (SUM(CLOSE, 8) / 8)
    x2 = STD(CLOSE, 8)
    t1 = x1 + x2
    t2 = (SUM(CLOSE, 2) / 2)
    t3 = x1 - x2
    t4 = (VOLUME / MEAN(VOLUME, 20))
    return IF(t1 < t2, -1, IF(t2 < t3, 1, IF(1 <= t4, 1, -1)))


def alpha_005(HIGH, VOLUME, **kwargs):
    """Alpha5 (-1 * TSMAX(CORR(TSRANK(VOLUME, 5), TSRANK(HIGH, 5), 5), 3))"""
    t1 = CORR(TSRANK(VOLUME, 5), TSRANK(HIGH, 5), 5)
    return (-1 * TSMAX(t1, 3))


def alpha_006(OPEN, HIGH, **kwargs):
    """Alpha6 (RANK(SIGN(DELTA((((OPEN * 0.85) + (HIGH * 0.15))), 4)))* -1)"""
    t1 = (((OPEN * 0.85) + (HIGH * 0.15)))
    return (RANK(SIGN(DELTA(t1, 4))) * -1)


def alpha_007(CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha7 ((RANK(MAX((VWAP - CLOSE), 3)) + RANK(MIN((VWAP - CLOSE), 3))) * RANK(DELTA(VOLUME, 3)))"""
    x0 = (VWAP - CLOSE)
    t1 = MAX(x0, 3)
    t2 = MIN(x0, 3)
    t3 = DELTA(VOLUME, 3)
    return ((RANK(t1) + RANK(t2)) * RANK(t3))


def alpha_008(HIGH, LOW, VWAP, **kwargs):
    """Alpha8 RANK(DELTA(((((HIGH + LOW) / 2) * 0.2) + (VWAP * 0.8)), 4) * -1)"""
    t1 = ((((HIGH + LOW) / 2) * 0.2) + (VWAP * 0.8))
    return RANK(DELTA(t1, 4) * -1)


def alpha_009(HIGH, LOW, VOLUME, **kwargs):
    """Alpha9 SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,7,2)"""
    t1 = ((HIGH + LOW) / 2 - (DELAY(HIGH, 1) + DELAY(LOW, 1)) / 2)
    return SMA(t1 * (HIGH - LOW) / VOLUME, 7, 2)


def alpha_010(CLOSE, RET, **kwargs):
    """Alpha10 (RANK(MAX(((RET < 0) ? STD(RET, 20) : CLOSE)^2),5))"""
    """Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)"""
    t1 = IF((RET < 0), STD(RET, 20), CLOSE)
    return (RANK(TSMAX(t1 ** 2, 5)))


def alpha_011(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha11 SUM(((CLOSE-LOW)-(HIGH-CLOSE))./(HIGH-LOW).*VOLUME,6)"""
    t1 = ((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)
    return SUM(t1 * VOLUME, 6)


def alpha_012(OPEN, CLOSE, VWAP, **kwargs):
    """Alpha12 (RANK((OPEN - (SUM(VWAP, 10) / 10)))) * (-1 * (RANK(ABS((CLOSE - VWAP)))))"""
    t1 = (SUM(VWAP, 10) / 10)
    return (RANK((OPEN - t1))) * (-1 * (RANK(ABS((CLOSE - VWAP)))))


def alpha_013(HIGH, LOW, VWAP, **kwargs):
    """Alpha13 (((HIGH * LOW)^0.5) - VWAP)"""
    return (((HIGH * LOW) ** 0.5) - VWAP)


def alpha_014(CLOSE, **kwargs):
    """Alpha14 CLOSE-DELAY(CLOSE,5)"""
    return CLOSE - DELAY(CLOSE, 5)


def alpha_015(OPEN, CLOSE, **kwargs):
    """Alpha15 OPEN/DELAY(CLOSE,1)-1"""
    return OPEN / DELAY(CLOSE, 1) - 1


def alpha_016(VOLUME, VWAP, **kwargs):
    """Alpha16 (-1 * TSMAX(RANK(CORR(RANK(VOLUME), RANK(VWAP), 5)), 5))"""
    t1 = CORR(RANK(VOLUME), RANK(VWAP), 5)
    return (-1 * TSMAX(RANK(t1), 5))


def alpha_017(CLOSE, VWAP, **kwargs):
    """Alpha17 RANK((VWAP - MAX(VWAP, 15)))^DELTA(CLOSE, 5)"""
    return RANK((VWAP - MAX(VWAP, 15))) ** DELTA(CLOSE, 5)


def alpha_018(CLOSE, **kwargs):
    """Alpha18 CLOSE/DELAY(CLOSE,5)"""
    return CLOSE / DELAY(CLOSE, 5)


def alpha_019(CLOSE, **kwargs):
    """Alpha19
(CLOSE<DELAY(CLOSE,5)?(CLOSE-DELAY(CLOSE,5))/DELAY(CLOSE,5):(CLOSE=DELAY(CLOSE,5)?0:(CLOSE-DELAY(CLOSE,5))/CLOSE))"""
    t1 = DELAY(CLOSE, 5)
    t2 = (CLOSE - t1)
    return IF(CLOSE < t1, t2 / t1, IF(CLOSE == t1, 0, t2 / CLOSE))


def alpha_020(CLOSE, **kwargs):
    """Alpha20 (CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*100"""
    t1 = DELAY(CLOSE, 6)
    return (CLOSE - t1) / t1 * 100


def alpha_021(CLOSE, **kwargs):
    """Alpha21 REGBETA(MEAN(CLOSE,6),SEQUENCE(6))"""
    return REGSLOPE(MEAN(CLOSE, 6), 6)


def alpha_022(CLOSE, **kwargs):
    """Alpha22 SMEAN(((CLOSE-MEAN(CLOSE,6))/MEAN(CLOSE,6)-DELAY((CLOSE-MEAN(CLOSE,6))/MEAN(CLOSE,6),3)),12,1)"""
    # 文档中的SMEAN可能是SMA
    t1 = MEAN(CLOSE, 6)
    t2 = (CLOSE - t1) / t1
    return SMA((t2 - DELAY(t2, 3)), 12, 1)


def alpha_023(CLOSE, **kwargs):
    """Alpha23
SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE:20),0),20,1)/(SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1
)+SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1))*100"""
    t1 = DELAY(CLOSE, 1)
    t2 = STD(CLOSE, 20)
    t3 = SMA(IF(CLOSE > t1, t2, 0), 20, 1)
    return t3 / (t3 + SMA(IF(CLOSE <= t1, t2, 0), 20, 1)) * 100


def alpha_024(CLOSE, **kwargs):
    """Alpha24 SMA(CLOSE-DELAY(CLOSE,5),5,1)"""
    return SMA(CLOSE - DELAY(CLOSE, 5), 5, 1)


def alpha_025(CLOSE, VOLUME, RET, **kwargs):
    """Alpha25
((-1 * RANK((DELTA(CLOSE, 7) * (1 - RANK(DECAYLINEAR((VOLUME / MEAN(VOLUME,20)), 9)))))) * (1 +
RANK(SUM(RET, 250))))"""
    t1 = (1 + RANK(SUM(RET, 250)))
    t2 = DECAYLINEAR((VOLUME / MEAN(VOLUME, 20)), 9)
    t3 = (DELTA(CLOSE, 7) * (1 - RANK(t2)))
    return ((-1 * RANK(t3)) * t1)


def alpha_026(CLOSE, VWAP, **kwargs):
    """Alpha26 ((((SUM(CLOSE, 7) / 7) - CLOSE)) + ((CORR(VWAP, DELAY(CLOSE, 5), 230))))"""
    t1 = (SUM(CLOSE, 7) / 7)
    t2 = CORR(VWAP, DELAY(CLOSE, 5), 230)
    return (((t1 - CLOSE)) + ((t2)))


def alpha_027(CLOSE, **kwargs):
    """Alpha27 WMA((CLOSE-DELAY(CLOSE,3))/DELAY(CLOSE,3)*100+(CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*100,12)"""
    t1 = DELAY(CLOSE, 3)
    t2 = DELAY(CLOSE, 6)
    return WMA((CLOSE - t1) / t1 * 100 + (CLOSE - t2) / t2 * 100, 12)


def alpha_028(HIGH, LOW, CLOSE, **kwargs):
    """Alpha28
3*SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)-2*SMA(SMA((CLOSE-TSMIN(LOW,9))/(
MAX(HIGH,9)-TSMAX(LOW,9))*100,3,1),3,1)"""
    t1 = TSMIN(LOW, 9)
    t2 = (CLOSE - t1) / (TSMAX(HIGH, 9) - t1) * 100
    t3 = (CLOSE - t1) / (MAX(HIGH, 9) - TSMAX(LOW, 9)) * 100
    return 3 * SMA(t2, 3, 1) - 2 * SMA(SMA(t3, 3, 1), 3, 1)


def alpha_029(CLOSE, VOLUME, **kwargs):
    """Alpha29 (CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*VOLUME"""
    t1 = DELAY(CLOSE, 6)
    return (CLOSE - t1) / t1 * VOLUME


def alpha_030(CLOSE, MKT, SMB, HML, **kwargs):
    """Alpha30 WMA((REGRESI(CLOSE/DELAY(CLOSE)-1,MKT,SMB,HML，60))^2,20)"""
    return WMA((REGRESI(CLOSE / DELAY(CLOSE, 1) - 1, MKT, SMB, HML, 60)) ** 2, 20)


def alpha_031(CLOSE, **kwargs):
    """Alpha31 (CLOSE-MEAN(CLOSE,12))/MEAN(CLOSE,12)*100"""
    t1 = MEAN(CLOSE, 12)
    return (CLOSE - t1) / t1 * 100


def alpha_032(HIGH, VOLUME, **kwargs):
    """Alpha32 (-1 * SUM(RANK(CORR(RANK(HIGH), RANK(VOLUME), 3)), 3))"""
    t1 = CORR(RANK(HIGH), RANK(VOLUME), 3)
    return (-1 * SUM(RANK(t1), 3))


def alpha_033(LOW, VOLUME, RET, **kwargs):
    """Alpha33
((((-1 * TSMIN(LOW, 5)) + DELAY(TSMIN(LOW, 5), 5)) * RANK(((SUM(RET, 240) - SUM(RET, 20)) / 220))) *
TSRANK(VOLUME, 5))"""
    t1 = TSMIN(LOW, 5)
    t2 = ((SUM(RET, 240) - SUM(RET, 20)) / 220)
    return ((((-1 * t1) + DELAY(t1, 5)) * RANK(t2)) * TSRANK(VOLUME, 5))


def alpha_034(CLOSE, **kwargs):
    """Alpha34 MEAN(CLOSE,12)/CLOSE"""
    return MEAN(CLOSE, 12) / CLOSE


def alpha_035(OPEN, VOLUME, **kwargs):
    """Alpha35
(MIN(RANK(DECAYLINEAR(DELTA(OPEN, 1), 15)), RANK(DECAYLINEAR(CORR((VOLUME), ((OPEN * 0.65) +
(OPEN *0.35)), 17),7))) * -1)"""
    t1 = DECAYLINEAR(DELTA(OPEN, 1), 15)
    t2 = DECAYLINEAR(CORR(VOLUME, OPEN, 17), 7)
    return (MIN(RANK(t1), RANK(t2)) * -1)


def alpha_036(VOLUME, VWAP, **kwargs):
    """Alpha36 RANK(SUM(CORR(RANK(VOLUME), RANK(VWAP)), 6), 2)"""
    """TODO 又有问题!!!"""
    t1 = CORR(RANK(VOLUME), RANK(VWAP), 6)
    return RANK(SUM(t1, 2))


def alpha_037(OPEN, RET, **kwargs):
    """Alpha37 (-1 * RANK(((SUM(OPEN, 5) * SUM(RET, 5)) - DELAY((SUM(OPEN, 5) * SUM(RET, 5)), 10))))"""
    t1 = (SUM(OPEN, 5) * SUM(RET, 5))
    return (-1 * RANK((t1 - DELAY(t1, 10))))


def alpha_038(HIGH, **kwargs):
    """Alpha38 (((SUM(HIGH, 20) / 20) < HIGH) ? (-1 * DELTA(HIGH, 2)) : 0)"""
    t1 = (SUM(HIGH, 20) / 20)
    return IF((t1 < HIGH), (-1 * DELTA(HIGH, 2)), 0)


def alpha_039(OPEN, CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha39
((RANK(DECAYLINEAR(DELTA((CLOSE), 2),8)) - RANK(DECAYLINEAR(CORR(((VWAP * 0.3) + (OPEN * 0.7)),
SUM(MEAN(VOLUME,180), 37), 14), 12))) * -1)"""
    t1 = DECAYLINEAR(DELTA((CLOSE), 2), 8)
    t2 = CORR(((VWAP * 0.3) + (OPEN * 0.7)), SUM(MEAN(VOLUME, 180), 37), 14)
    t3 = DECAYLINEAR(t2, 12)
    return ((RANK(t1) - RANK(t3)) * -1)


def alpha_040(CLOSE, VOLUME, **kwargs):
    """Alpha40 SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:0),26)/SUM((CLOSE<=DELAY(CLOSE,1)?VOLUME:0),26)*100"""
    t1 = DELAY(CLOSE, 1)
    return SUM(IF(CLOSE > t1, VOLUME, 0), 26) / SUM(IF(CLOSE <= t1, VOLUME, 0), 26) * 100


def alpha_041(VWAP, **kwargs):
    """Alpha41 (RANK(MAX(DELTA((VWAP), 3), 5))* -1)"""
    return (RANK(MAX(DELTA((VWAP), 3), 5)) * -1)


def alpha_042(HIGH, VOLUME, **kwargs):
    """Alpha42 ((-1 * RANK(STD(HIGH, 10))) * CORR(HIGH, VOLUME, 10))"""
    return ((-1 * RANK(STD(HIGH, 10))) * CORR(HIGH, VOLUME, 10))


def alpha_043(CLOSE, VOLUME, **kwargs):
    """Alpha43 SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),6)"""
    t1 = DELAY(CLOSE, 1)
    return SUM(IF(CLOSE > t1, VOLUME, IF(CLOSE < t1, -VOLUME, 0)), 6)


def alpha_044(LOW, VOLUME, VWAP, **kwargs):
    """Alpha44
(TSRANK(DECAYLINEAR(CORR(((LOW )), MEAN(VOLUME,10), 7), 6),4) + TSRANK(DECAYLINEAR(DELTA((VWAP),
3), 10), 15))"""
    t1 = DECAYLINEAR(CORR(LOW, MEAN(VOLUME, 10), 7), 6)
    t2 = DECAYLINEAR(DELTA(VWAP, 3), 10)
    return (TSRANK(t1, 4) + TSRANK(t2, 15))


def alpha_045(OPEN, CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha45 (RANK(DELTA((((CLOSE * 0.6) + (OPEN *0.4))), 1)) * RANK(CORR(VWAP, MEAN(VOLUME,150), 15)))"""
    t1 = DELTA((((CLOSE * 0.6) + (OPEN * 0.4))), 1)
    t2 = CORR(VWAP, MEAN(VOLUME, 150), 15)
    return (RANK(t1) * RANK(t2))


def alpha_046(CLOSE, **kwargs):
    """Alpha46 (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/(4*CLOSE)"""
    return (MEAN(CLOSE, 3) + MEAN(CLOSE, 6) + MEAN(CLOSE, 12) + MEAN(CLOSE, 24)) / (4 * CLOSE)


def alpha_047(HIGH, LOW, CLOSE, **kwargs):
    """Alpha47 SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,9,1)"""
    t1 = TSMAX(HIGH, 6)
    t2 = TSMIN(LOW, 6)
    return SMA((t1 - CLOSE) / (t1 - t2) * 100, 9, 1)


def alpha_048(CLOSE, VOLUME, **kwargs):
    """Alpha48
(-1*((RANK(((SIGN((CLOSE - DELAY(CLOSE, 1))) + SIGN((DELAY(CLOSE, 1) - DELAY(CLOSE, 2)))) +
SIGN((DELAY(CLOSE, 2) - DELAY(CLOSE, 3)))))) * SUM(VOLUME, 5)) / SUM(VOLUME, 20))"""
    t1 = DELAY(CLOSE, 1)
    t2 = DELAY(CLOSE, 2)
    t3 = DELAY(CLOSE, 3)
    t4 = SUM(VOLUME, 5) / SUM(VOLUME, 20)
    return (-1 * (RANK(((SIGN((CLOSE - t1)) + SIGN((t1 - t2))) + SIGN((t2 - t3))))) * t4)


def alpha_049(HIGH, LOW, **kwargs):
    """Alpha49
SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(L
OW,1)))),12)/(SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(L
OW-DELAY(LOW,1)))),12)+SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HI
GH,1)),ABS(LOW-DELAY(LOW,1)))),12))"""
    t1 = MAX(ABS(HIGH - DELAY(HIGH, 1)), ABS(LOW - DELAY(LOW, 1)))
    t2 = (DELAY(HIGH, 1) + DELAY(LOW, 1))
    t3 = (HIGH + LOW)
    t4 = SUM(IF(t3 >= t2, 0, t1), 12)
    t5 = SUM(IF(t3 <= t2, 0, t1), 12)
    return t4 / (t4 + t5)


def alpha_050(HIGH, LOW, **kwargs):
    """Alpha50
SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(L
OW,1)))),12)/(SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(L
OW-DELAY(LOW,1)))),12)+SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HI
GH,1)),ABS(LOW-DELAY(LOW,1)))),12))-SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HI
GH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)/(SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:
MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)+SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELA
Y(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12))"""
    t1 = MAX(ABS(HIGH - DELAY(HIGH, 1)), ABS(LOW - DELAY(LOW, 1)))
    t2 = (DELAY(HIGH, 1) + DELAY(LOW, 1))
    t3 = (HIGH + LOW)
    t4 = SUM(IF(t3 <= t2, 0, t1), 12)
    t5 = SUM(IF(t3 >= t2, 0, t1), 12)
    return (t4 - t5) / (t4 + t5)


def alpha_051(HIGH, LOW, **kwargs):
    """Alpha51
SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(L
OW,1)))),12)/(SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(L
OW-DELAY(LOW,1)))),12)+SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HI
GH,1)),ABS(LOW-DELAY(LOW,1)))),12))"""
    t1 = MAX(ABS(HIGH - DELAY(HIGH, 1)), ABS(LOW - DELAY(LOW, 1)))
    t2 = (DELAY(HIGH, 1) + DELAY(LOW, 1))
    t3 = (HIGH + LOW)
    t4 = SUM(IF(t3 <= t2, 0, t1), 12)
    t5 = SUM(IF(t3 >= t2, 0, t1), 12)
    return t4 / (t4 + t5)


def alpha_052(HIGH, LOW, CLOSE, **kwargs):
    """Alpha52
SUM(MAX(0,HIGH-DELAY((HIGH+LOW+CLOSE)/3,1)),26)/SUM(MAX(0,DELAY((HIGH+LOW+CLOSE)/3,1)-L),26)*
100"""
    # L应当是LOW
    t1 = DELAY((HIGH + LOW + CLOSE) / 3, 1)
    t2 = MAX(0, HIGH - t1)
    t3 = MAX(0, t1 - LOW)
    return SUM(t2, 26) / SUM(t3, 26) * 100


def alpha_053(CLOSE, **kwargs):
    """Alpha53 COUNT(CLOSE>DELAY(CLOSE,1),12)/12*100"""
    return COUNT(CLOSE > DELAY(CLOSE, 1), 12) / 12 * 100


def alpha_054(OPEN, CLOSE, **kwargs):
    """Alpha54 (-1 * RANK((STD(ABS(CLOSE - OPEN)) + (CLOSE - OPEN)) + CORR(CLOSE, OPEN,10)))"""
    """Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))"""
    t1 = (STD(ABS(CLOSE - OPEN), 5) + (CLOSE - OPEN))
    t2 = CORR(CLOSE, OPEN, 10)
    return (-1 * RANK(t1 + t2))


def alpha_055(OPEN, HIGH, LOW, CLOSE, **kwargs):
    """Alpha55
SUM(16*(CLOSE-DELAY(CLOSE,1)+(CLOSE-OPEN)/2+DELAY(CLOSE,1)-DELAY(OPEN,1))/((ABS(HIGH-DELAY(CL
OSE,1))>ABS(LOW-DELAY(CLOSE,1)) &
ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1))?ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOS
E,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:(ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) &
ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1))?ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLO
SE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OP
EN,1))/4)))*MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1))),20)"""
    t1 = ABS(HIGH - DELAY(CLOSE, 1))
    t2 = ABS(LOW - DELAY(CLOSE, 1))
    t3 = ABS(HIGH - DELAY(LOW, 1))
    t4 = ABS(DELAY(CLOSE, 1) - DELAY(OPEN, 1))
    return SUM(16 * (CLOSE + (CLOSE - OPEN) / 2 - DELAY(OPEN, 1)) /
               (IF((t1 > t2) & (t1 > t3),
                   t1 + t2 / 2 + t4 / 4,
                   IF((t2 > t3) & (t2 > t1),
                      t2 + t1 / 2 + t4 / 4,
                      t3 + t4 / 4))) *
               MAX(t1, t2),
               20)


def alpha_056(OPEN, HIGH, LOW, VOLUME, **kwargs):
    """Alpha56
(RANK((OPEN - TSMIN(OPEN, 12))) < RANK((RANK(CORR(SUM(((HIGH + LOW) / 2), 19),
SUM(MEAN(VOLUME,40), 19), 13))^5)))"""
    t1 = CORR(SUM(((HIGH + LOW) / 2), 19), SUM(MEAN(VOLUME, 40), 19), 13)
    return LessThan(RANK((OPEN - TSMIN(OPEN, 12))),
                    RANK((RANK(t1) ** 5)))


def alpha_057(HIGH, LOW, CLOSE, **kwargs):
    """Alpha57 SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)"""
    t1 = TSMIN(LOW, 9)
    t2 = TSMAX(HIGH, 9)
    return SMA((CLOSE - t1) / (t2 - t1) * 100, 3, 1)


def alpha_058(CLOSE, **kwargs):
    """Alpha58 COUNT(CLOSE>DELAY(CLOSE,1),20)/20*100"""
    return COUNT(CLOSE > DELAY(CLOSE, 1), 20) / 20 * 100


def alpha_059(HIGH, LOW, CLOSE, **kwargs):
    """Alpha59
SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,D
ELAY(CLOSE,1)))),20)"""
    t0 = DELAY(CLOSE, 1)
    t1 = IF(CLOSE > t0, MIN(LOW, t0), MAX(HIGH, t0))
    return SUM(IF(CLOSE == t0, 0, CLOSE - t1), 20)


def alpha_060(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha60 SUM(((CLOSE-LOW)-(HIGH-CLOSE))./(HIGH-LOW).*VOLUME,20)"""
    return SUM(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW) * VOLUME, 20)


def alpha_061(LOW, VOLUME, VWAP, **kwargs):
    """Alpha61
(MAX(RANK(DECAYLINEAR(DELTA(VWAP, 1), 12)),
RANK(DECAYLINEAR(RANK(CORR((LOW),MEAN(VOLUME,80), 8)), 17))) * -1)"""
    t1 = DECAYLINEAR(DELTA(VWAP, 1), 12)
    t2 = DECAYLINEAR(RANK(CORR(LOW, MEAN(VOLUME, 80), 8)), 17)
    return (MAX(RANK(t1), RANK(t2)) * -1)


def alpha_062(HIGH, VOLUME, **kwargs):
    """Alpha62 (-1 * CORR(HIGH, RANK(VOLUME), 5))"""
    return (-1 * CORR(HIGH, RANK(VOLUME), 5))


def alpha_063(CLOSE, **kwargs):
    """Alpha63 SMA(MAX(CLOSE-DELAY(CLOSE,1),0),6,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),6,1)*100"""
    t1 = CLOSE - DELAY(CLOSE, 1)
    return SMA(MAX(t1, 0), 6, 1) / SMA(ABS(t1), 6, 1) * 100


def alpha_064(CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha64
(MAX(RANK(DECAYLINEAR(CORR(RANK(VWAP), RANK(VOLUME), 4), 4)),
RANK(DECAYLINEAR(MAX(CORR(RANK(CLOSE), RANK(MEAN(VOLUME,60)), 4), 13), 14))) * -1)"""
    t1 = DECAYLINEAR(CORR(RANK(VWAP), RANK(VOLUME), 4), 4)
    t2 = DECAYLINEAR(MAX(CORR(RANK(CLOSE), RANK(MEAN(VOLUME, 60)), 4), 13), 14)
    return (MAX(RANK(t1), RANK(t2)) * -1)


def alpha_065(CLOSE, **kwargs):
    """Alpha65 MEAN(CLOSE,6)/CLOSE"""
    return MEAN(CLOSE, 6) / CLOSE


def alpha_066(CLOSE, **kwargs):
    """Alpha66 (CLOSE-MEAN(CLOSE,6))/MEAN(CLOSE,6)*100"""
    t1 = MEAN(CLOSE, 6)
    return (CLOSE - t1) / t1 * 100


def alpha_067(CLOSE, **kwargs):
    """Alpha67 SMA(MAX(CLOSE-DELAY(CLOSE,1),0),24,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),24,1)*100"""
    t1 = CLOSE - DELAY(CLOSE, 1)
    return SMA(MAX(t1, 0), 24, 1) / SMA(ABS(t1), 24, 1) * 100


def alpha_068(HIGH, LOW, VOLUME, **kwargs):
    """Alpha68 SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,15,2)"""
    t1 = (HIGH + LOW)
    t2 = (DELAY(HIGH, 1) + DELAY(LOW, 1))
    return SMA((t1 / 2 - t2 / 2) * (HIGH - LOW) / VOLUME, 15, 2)


def alpha_069(DTM, DBM, **kwargs):
    """Alpha69
(SUM(DTM,20)>SUM(DBM,20)？(SUM(DTM,20)-SUM(DBM,20))/SUM(DTM,20)：(SUM(DTM,20)=SUM(DBM,20)？ 0：(SUM(DTM,20)-SUM(DBM,20))/SUM(DBM,20)))"""
    t1 = SUM(DTM, 20)
    t2 = SUM(DBM, 20)
    return IF(t1 > t2, (t1 - t2) / t1, IF(t1 == t2, 0, (t1 - t2) / t2))


def alpha_070(AMOUNT, **kwargs):
    """Alpha70 STD(AMOUNT,6)"""
    return STD(AMOUNT, 6)


def alpha_071(CLOSE, **kwargs):
    """Alpha71 (CLOSE-MEAN(CLOSE,24))/MEAN(CLOSE,24)*100"""
    t1 = MEAN(CLOSE, 24)
    return (CLOSE - t1) / t1 * 100


def alpha_072(HIGH, LOW, CLOSE, **kwargs):
    """Alpha72 SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,15,1)"""
    t1 = TSMAX(HIGH, 6)
    t2 = TSMIN(LOW, 6)
    return SMA((t1 - CLOSE) / (t1 - t2) * 100, 15, 1)


def alpha_073(CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha73
((TSRANK(DECAYLINEAR(DECAYLINEAR(CORR((CLOSE), VOLUME, 10), 16), 4), 5) -
RANK(DECAYLINEAR(CORR(VWAP, MEAN(VOLUME,30), 4),3))) * -1)"""
    t1 = DECAYLINEAR(DECAYLINEAR(CORR((CLOSE), VOLUME, 10), 16), 4)
    t2 = DECAYLINEAR(CORR(VWAP, MEAN(VOLUME, 30), 4), 3)
    return ((TSRANK(t1, 5) - RANK(t2)) * -1)


def alpha_074(LOW, VOLUME, VWAP, **kwargs):
    """Alpha74
(RANK(CORR(SUM(((LOW * 0.35) + (VWAP * 0.65)), 20), SUM(MEAN(VOLUME,40), 20), 7)) +
RANK(CORR(RANK(VWAP), RANK(VOLUME), 6)))"""
    t1 = CORR(SUM(((LOW * 0.35) + (VWAP * 0.65)), 20), SUM(MEAN(VOLUME, 40), 20), 7)
    t2 = CORR(RANK(VWAP), RANK(VOLUME), 6)
    return (RANK(t1) +
            RANK(t2))


def alpha_075(OPEN, CLOSE, BANCHMARKINDEXOPEN, BANCHMARKINDEXCLOSE, **kwargs):
    """Alpha75
COUNT(CLOSE>OPEN &
BANCHMARKINDEXCLOSE<BANCHMARKINDEXOPEN,50)/COUNT(BANCHMARKINDEXCLOSE<BANCHMARKIN
DEXOPEN,50)"""
    t1 = BANCHMARKINDEXCLOSE < BANCHMARKINDEXOPEN
    return COUNT((CLOSE > OPEN) & t1, 50) / COUNT(t1, 50)


def alpha_076(CLOSE, VOLUME, **kwargs):
    """Alpha76 STD(ABS((CLOSE/DELAY(CLOSE,1)-1))/VOLUME,20)/MEAN(ABS((CLOSE/DELAY(CLOSE,1)-1))/VOLUME,20)"""
    t1 = ABS((CLOSE / DELAY(CLOSE, 1) - 1)) / VOLUME
    return STD(t1, 20) / MEAN(t1, 20)


def alpha_077(HIGH, LOW, VOLUME, VWAP, **kwargs):
    """Alpha77
MIN(RANK(DECAYLINEAR(((((HIGH + LOW) / 2) + HIGH) - (VWAP + HIGH)), 20)),
RANK(DECAYLINEAR(CORR(((HIGH + LOW) / 2), MEAN(VOLUME,40), 3), 6)))"""
    t1 = DECAYLINEAR(((((HIGH + LOW) / 2) + HIGH) - (VWAP + HIGH)), 20)
    t2 = DECAYLINEAR(CORR(((HIGH + LOW) / 2), MEAN(VOLUME, 40), 3), 6)
    return MIN(RANK(t1), RANK(t2))


def alpha_078(HIGH, LOW, CLOSE, **kwargs):
    """Alpha78
((HIGH+LOW+CLOSE)/3-MA((HIGH+LOW+CLOSE)/3,12))/(0.015*MEAN(ABS(CLOSE-MEAN((HIGH+LOW+CLOS
E)/3,12)),12))"""
    t1 = (HIGH + LOW + CLOSE) / 3
    return (t1 - MA(t1, 12)) / (0.015 * MEAN(ABS(CLOSE - MEAN(t1, 12)), 12))


def alpha_079(CLOSE, **kwargs):
    """Alpha79 SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100"""
    t1 = CLOSE - DELAY(CLOSE, 1)
    return SMA(MAX(t1, 0), 12, 1) / SMA(ABS(t1), 12, 1) * 100


def alpha_080(VOLUME, **kwargs):
    """Alpha80 (VOLUME-DELAY(VOLUME,5))/DELAY(VOLUME,5)*100"""
    t1 = DELAY(VOLUME, 5)
    return (VOLUME - t1) / t1 * 100


def alpha_081(VOLUME, **kwargs):
    """Alpha81 SMA(VOLUME,21,2)"""
    return SMA(VOLUME, 21, 2)


def alpha_082(HIGH, LOW, CLOSE, **kwargs):
    """Alpha82 SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,20,1)"""
    t1 = TSMAX(HIGH, 6)
    t2 = TSMIN(LOW, 6)
    return SMA((t1 - CLOSE) / (t1 - t2) * 100, 20, 1)


def alpha_083(HIGH, VOLUME, **kwargs):
    """Alpha83 (-1 * RANK(COVIANCE(RANK(HIGH), RANK(VOLUME), 5)))"""
    t1 = COVIANCE(RANK(HIGH), RANK(VOLUME), 5)
    return (-1 * RANK(t1))


def alpha_084(CLOSE, VOLUME, **kwargs):
    """Alpha84 SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),20)"""
    t1 = DELAY(CLOSE, 1)
    return SUM(IF(CLOSE > t1, VOLUME, IF(CLOSE < t1, -VOLUME, 0)), 20)


def alpha_085(CLOSE, VOLUME, **kwargs):
    """Alpha85 (TSRANK((VOLUME / MEAN(VOLUME,20)), 20) * TSRANK((-1 * DELTA(CLOSE, 7)), 8))"""
    t1 = (VOLUME / MEAN(VOLUME, 20))
    t2 = (-1 * DELTA(CLOSE, 7))
    return (TSRANK(t1, 20) * TSRANK(t2, 8))


def alpha_086(CLOSE, **kwargs):
    """Alpha86
((0.25 < (((DELAY(CLOSE, 20) - DELAY(CLOSE, 10)) / 10) - ((DELAY(CLOSE, 10) - CLOSE) / 10))) ? (-1 * 1) :
(((((DELAY(CLOSE, 20) - DELAY(CLOSE, 10)) / 10) - ((DELAY(CLOSE, 10) - CLOSE) / 10)) < 0) ? 1 : ((-1 * 1) *
(CLOSE - DELAY(CLOSE, 1)))))"""
    t1 = DELAY(CLOSE, 20)
    t2 = DELAY(CLOSE, 10)
    t3 = DELAY(CLOSE, 1)
    t4 = (((t1 - t2) / 10) - ((t2 - CLOSE) / 10))
    return IF((0.25 < t4), -1, IF((t4 < 0), 1, (-1 * (CLOSE - t3))))


def alpha_087(OPEN, HIGH, LOW, VWAP, **kwargs):
    """Alpha87
((RANK(DECAYLINEAR(DELTA(VWAP, 4), 7)) + TSRANK(DECAYLINEAR(((((LOW * 0.9) + (LOW * 0.1)) - VWAP) /
(OPEN - ((HIGH + LOW) / 2))), 11), 7)) * -1)"""
    t1 = DECAYLINEAR(DELTA(VWAP, 4), 7)
    t2 = DECAYLINEAR(((LOW - VWAP) / (OPEN - ((HIGH + LOW) / 2))), 11)
    return ((RANK(t1) + TSRANK(t2, 7)) * -1)


def alpha_088(CLOSE, **kwargs):
    """Alpha88 (CLOSE-DELAY(CLOSE,20))/DELAY(CLOSE,20)*100"""
    t1 = DELAY(CLOSE, 20)
    return (CLOSE - t1) / t1 * 100


def alpha_089(CLOSE, **kwargs):
    """Alpha89 2*(SMA(CLOSE,13,2)-SMA(CLOSE,27,2)-SMA(SMA(CLOSE,13,2)-SMA(CLOSE,27,2),10,2))"""
    t1 = SMA(CLOSE, 13, 2) - SMA(CLOSE, 27, 2)
    return 2 * (t1 - SMA(t1, 10, 2))


def alpha_090(VOLUME, VWAP, **kwargs):
    """Alpha90 ( RANK(CORR(RANK(VWAP), RANK(VOLUME), 5)) * -1)"""
    t1 = CORR(RANK(VWAP), RANK(VOLUME), 5)
    return (RANK(t1) * -1)


def alpha_091(LOW, CLOSE, VOLUME, **kwargs):
    """Alpha91 ((RANK((CLOSE - MAX(CLOSE, 5)))*RANK(CORR((MEAN(VOLUME,40)), LOW, 5))) * -1)"""
    t1 = (CLOSE - MAX(CLOSE, 5))
    t2 = CORR((MEAN(VOLUME, 40)), LOW, 5)
    return ((RANK(t1) * RANK(t2)) * -1)


def alpha_092(CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha92
(MAX(RANK(DECAYLINEAR(DELTA(((CLOSE * 0.35) + (VWAP *0.65)), 2), 3)),
TSRANK(DECAYLINEAR(ABS(CORR((MEAN(VOLUME,180)), CLOSE, 13)), 5), 15)) * -1)"""
    t1 = DECAYLINEAR(DELTA(((CLOSE * 0.35) + (VWAP * 0.65)), 2), 3)
    t2 = DECAYLINEAR(ABS(CORR((MEAN(VOLUME, 180)), CLOSE, 13)), 5)
    return (MAX(RANK(t1),
                TSRANK(t2, 15)) * -1)


def alpha_093(OPEN, LOW, **kwargs):
    """Alpha93 SUM((OPEN>=DELAY(OPEN,1)?0:MAX((OPEN-LOW),(OPEN-DELAY(OPEN,1)))),20)"""
    t1 = DELAY(OPEN, 1)
    t2 = MAX((OPEN - LOW), (OPEN - t1))
    return SUM(IF(OPEN >= t1, 0, t2), 20)


def alpha_094(CLOSE, VOLUME, **kwargs):
    """Alpha94 SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),30)"""
    t1 = DELAY(CLOSE, 1)
    return SUM(IF(CLOSE > t1, VOLUME, IF(CLOSE < t1, -VOLUME, 0)), 30)


def alpha_095(AMOUNT, **kwargs):
    """Alpha95 STD(AMOUNT,20)"""
    return STD(AMOUNT, 20)


def alpha_096(HIGH, LOW, CLOSE, **kwargs):
    """Alpha96 SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)"""
    t1 = TSMIN(LOW, 9)
    t2 = TSMAX(HIGH, 9)
    return SMA(SMA((CLOSE - t1) / (t2 - t1) * 100, 3, 1), 3, 1)


def alpha_097(VOLUME, **kwargs):
    """Alpha97 STD(VOLUME,10)"""
    return STD(VOLUME, 10)


def alpha_098(CLOSE, **kwargs):
    """Alpha98
((((DELTA((SUM(CLOSE, 100) / 100), 100) / DELAY(CLOSE, 100)) < 0.05) || ((DELTA((SUM(CLOSE, 100) / 100), 100) /
DELAY(CLOSE, 100)) == 0.05)) ? (-1 * (CLOSE - TSMIN(CLOSE, 100))) : (-1 * DELTA(CLOSE, 3)))"""
    t1 = DELTA((SUM(CLOSE, 100) / 100), 100)
    return IF(((t1 / DELAY(CLOSE, 100)) <= 0.05), (-1 * (CLOSE - TSMIN(CLOSE, 100))), (-1 * DELTA(CLOSE, 3)))


def alpha_099(CLOSE, VOLUME, **kwargs):
    """Alpha99 (-1 * RANK(COVIANCE(RANK(CLOSE), RANK(VOLUME), 5)))"""
    t1 = COVIANCE(RANK(CLOSE), RANK(VOLUME), 5)
    return (-1 * RANK(t1))


def alpha_100(VOLUME, **kwargs):
    """Alpha100 STD(VOLUME,20)"""
    return STD(VOLUME, 20)


def alpha_101(HIGH, CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha101
((RANK(CORR(CLOSE, SUM(MEAN(VOLUME,30), 37), 15)) < RANK(CORR(RANK(((HIGH * 0.1) + (VWAP * 0.9))),
RANK(VOLUME), 11))) * -1)"""
    t1 = CORR(CLOSE, SUM(MEAN(VOLUME, 30), 37), 15)
    t2 = CORR(RANK(((HIGH * 0.1) + (VWAP * 0.9))), RANK(VOLUME), 11)
    return (LessThan(RANK(t1),
                     RANK(t2)) * -1)


def alpha_102(VOLUME, **kwargs):
    """Alpha102 SMA(MAX(VOLUME-DELAY(VOLUME,1),0),6,1)/SMA(ABS(VOLUME-DELAY(VOLUME,1)),6,1)*100"""
    t1 = DELAY(VOLUME, 1)
    return SMA(MAX(VOLUME - t1, 0), 6, 1) / SMA(ABS(VOLUME - t1), 6, 1) * 100


def alpha_103(LOW, **kwargs):
    """Alpha103 ((20-LOWDAY(LOW,20))/20)*100"""
    return ((20 - LOWDAY(LOW, 20)) / 20) * 100


def alpha_104(HIGH, CLOSE, VOLUME, **kwargs):
    """Alpha104 (-1 * (DELTA(CORR(HIGH, VOLUME, 5), 5) * RANK(STD(CLOSE, 20))))"""
    return (-1 * (DELTA(CORR(HIGH, VOLUME, 5), 5) * RANK(STD(CLOSE, 20))))


def alpha_105(OPEN, VOLUME, **kwargs):
    """Alpha105 (-1 * CORR(RANK(OPEN), RANK(VOLUME), 10))"""
    return (-1 * CORR(RANK(OPEN), RANK(VOLUME), 10))


def alpha_106(CLOSE, **kwargs):
    """Alpha106 CLOSE-DELAY(CLOSE,20)"""
    return CLOSE - DELAY(CLOSE, 20)


def alpha_107(OPEN, HIGH, LOW, CLOSE, **kwargs):
    """Alpha107 (((-1 * RANK((OPEN - DELAY(HIGH, 1)))) * RANK((OPEN - DELAY(CLOSE, 1)))) * RANK((OPEN - DELAY(LOW, 1))))"""
    t1 = (OPEN - DELAY(HIGH, 1))
    t2 = (OPEN - DELAY(CLOSE, 1))
    t3 = (OPEN - DELAY(LOW, 1))
    return (((-1 * RANK(t1)) * RANK(t2)) * RANK(t3))


def alpha_108(HIGH, VOLUME, VWAP, **kwargs):
    """Alpha108 ((RANK((HIGH - MIN(HIGH, 2)))^RANK(CORR((VWAP), (MEAN(VOLUME,120)), 6))) * -1)"""
    t1 = (HIGH - MIN(HIGH, 2))
    t2 = CORR((VWAP), (MEAN(VOLUME, 120)), 6)
    return ((RANK(t1) ** RANK(t2)) * -1)


def alpha_109(HIGH, LOW, **kwargs):
    """Alpha109 SMA(HIGH-LOW,10,2)/SMA(SMA(HIGH-LOW,10,2),10,2)"""
    t1 = SMA(HIGH - LOW, 10, 2)
    return t1 / SMA(t1, 10, 2)


def alpha_110(HIGH, LOW, CLOSE, **kwargs):
    """Alpha110 SUM(MAX(0,HIGH-DELAY(CLOSE,1)),20)/SUM(MAX(0,DELAY(CLOSE,1)-LOW),20)*100"""
    t1 = DELAY(CLOSE, 1)
    return SUM(MAX(0, HIGH - t1), 20) / SUM(MAX(0, t1 - LOW), 20) * 100


def alpha_111(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha111
SMA(VOL*((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-LOW),11,2)-SMA(VOL*((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-L
OW),4,2)"""
    t1 = VOLUME * ((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)
    return (SMA(t1, 11, 2) -
            SMA(t1, 4, 2))


def alpha_112(CLOSE, **kwargs):
    """Alpha112
(SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)-SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOS
E-DELAY(CLOSE,1)):0),12))/(SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)+SUM((CLOSE-DE
LAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))*100"""
    t1 = CLOSE - DELAY(CLOSE, 1)
    t2 = SUM(IF(t1 > 0, t1, 0), 12)
    t3 = SUM(IF(t1 < 0, ABS(t1), 0), 12)
    return ((t2 - t3) /
            (t2 + t3) * 100)


def alpha_113(CLOSE, VOLUME, **kwargs):
    """Alpha113
(-1 * ((RANK((SUM(DELAY(CLOSE, 5), 20) / 20)) * CORR(CLOSE, VOLUME, 2)) * RANK(CORR(SUM(CLOSE, 5),
SUM(CLOSE, 20), 2))))"""
    t1 = (SUM(DELAY(CLOSE, 5), 20) / 20)
    t2 = CORR(SUM(CLOSE, 5), SUM(CLOSE, 20), 2)
    return (-1 * ((RANK(t1) * CORR(CLOSE, VOLUME, 2)) * RANK(t2)))


def alpha_114(HIGH, LOW, CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha114
((RANK(DELAY(((HIGH - LOW) / (SUM(CLOSE, 5) / 5)), 2)) * RANK(RANK(VOLUME))) / (((HIGH - LOW) /
(SUM(CLOSE, 5) / 5)) / (VWAP - CLOSE)))"""
    t1 = ((HIGH - LOW) / (SUM(CLOSE, 5) / 5))
    return ((RANK(DELAY(t1, 2)) * RANK(VOLUME)) /
            (t1 / (VWAP - CLOSE)))


def alpha_115(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha115
(RANK(CORR(((HIGH * 0.9) + (CLOSE * 0.1)), MEAN(VOLUME,30), 10))^RANK(CORR(TSRANK(((HIGH + LOW) /
2), 4), TSRANK(VOLUME, 10), 7)))"""
    t1 = CORR(((HIGH * 0.9) + (CLOSE * 0.1)), MEAN(VOLUME, 30), 10)
    t2 = CORR(TSRANK(((HIGH + LOW) / 2), 4), TSRANK(VOLUME, 10), 7)
    return (RANK(t1) ** RANK(t2))


def alpha_116(CLOSE, **kwargs):
    """Alpha116 REGBETA(CLOSE,SEQUENCE,20)"""
    return REGSLOPE(CLOSE, 20)


def alpha_117(HIGH, LOW, CLOSE, VOLUME, RET, **kwargs):
    """Alpha117 ((TSRANK(VOLUME, 32) * (1 - TSRANK(((CLOSE + HIGH) - LOW), 16))) * (1 - TSRANK(RET, 32)))"""
    t1 = ((CLOSE + HIGH) - LOW)
    return ((TSRANK(VOLUME, 32) * (1 - TSRANK(t1, 16))) * (1 - TSRANK(RET, 32)))


def alpha_118(OPEN, HIGH, LOW, **kwargs):
    """Alpha118 SUM(HIGH-OPEN,20)/SUM(OPEN-LOW,20)*100"""
    return SUM(HIGH - OPEN, 20) / SUM(OPEN - LOW, 20) * 100


def alpha_119(OPEN, VOLUME, VWAP, **kwargs):
    """Alpha119
(RANK(DECAYLINEAR(CORR(VWAP, SUM(MEAN(VOLUME,5), 26), 5), 7)) -
RANK(DECAYLINEAR(TSRANK(MIN(CORR(RANK(OPEN), RANK(MEAN(VOLUME,15)), 21), 9), 7), 8)))"""
    t1 = CORR(VWAP, SUM(MEAN(VOLUME, 5), 26), 5)
    t2 = TSRANK(MIN(CORR(RANK(OPEN), RANK(MEAN(VOLUME, 15)), 21), 9), 7)
    return (RANK(DECAYLINEAR(t1, 7)) -
            RANK(DECAYLINEAR(t2, 8)))


def alpha_120(CLOSE, VWAP, **kwargs):
    """Alpha120 (RANK((VWAP - CLOSE)) / RANK((VWAP + CLOSE)))"""
    return (RANK((VWAP - CLOSE)) / RANK((VWAP + CLOSE)))


def alpha_121(VOLUME, VWAP, **kwargs):
    """Alpha121
((RANK((VWAP - MIN(VWAP, 12)))^TSRANK(CORR(TSRANK(VWAP, 20), TSRANK(MEAN(VOLUME,60), 2), 18), 3)) *
-1)"""
    t1 = (VWAP - MIN(VWAP, 12))
    t2 = CORR(TSRANK(VWAP, 20), TSRANK(MEAN(VOLUME, 60), 2), 18)
    return ((RANK(t1) ** TSRANK(t2, 3)) * -1)


def alpha_122(CLOSE, **kwargs):
    """Alpha122
(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)-DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1))/DELAY(SM
A(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1)"""
    t1 = SMA(SMA(SMA(LOG(CLOSE), 13, 2), 13, 2), 13, 2)
    t2 = DELAY(t1, 1)
    return ((t1 - t2) / t2)


def alpha_123(HIGH, LOW, VOLUME, **kwargs):
    """Alpha123
((RANK(CORR(SUM(((HIGH + LOW) / 2), 20), SUM(MEAN(VOLUME,60), 20), 9)) < RANK(CORR(LOW, VOLUME,
6))) * -1)"""
    t1 = CORR(SUM(((HIGH + LOW) / 2), 20), SUM(MEAN(VOLUME, 60), 20), 9)
    t2 = CORR(LOW, VOLUME, 6)
    return (LessThan(RANK(t1),
                     RANK(t2)) * -1)


def alpha_124(CLOSE, VWAP, **kwargs):
    """Alpha124 (CLOSE - VWAP) / DECAYLINEAR(RANK(TSMAX(CLOSE, 30)),2)"""
    return (CLOSE - VWAP) / DECAYLINEAR(RANK(TSMAX(CLOSE, 30)), 2)


def alpha_125(CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha125
(RANK(DECAYLINEAR(CORR((VWAP), MEAN(VOLUME,80),17), 20)) / RANK(DECAYLINEAR(DELTA(((CLOSE * 0.5)
+ (VWAP * 0.5)), 3), 16)))"""
    t1 = CORR((VWAP), MEAN(VOLUME, 80), 17)
    t2 = DELTA(((CLOSE * 0.5) + (VWAP * 0.5)), 3)
    return (RANK(DECAYLINEAR(t1, 20)) /
            RANK(DECAYLINEAR(t2, 16)))


def alpha_126(HIGH, LOW, CLOSE, **kwargs):
    """Alpha126 (CLOSE+HIGH+LOW)/3"""
    return (CLOSE + HIGH + LOW) / 3


def alpha_127(CLOSE, **kwargs):
    """Alpha127 (MEAN((100*(CLOSE-MAX(CLOSE,12))/(MAX(CLOSE,12)))^2))^(1/2)"""
    """!!!原公式有问题，补了12"""
    t1 = TSMAX(CLOSE, 12)
    return (MEAN((100 * (CLOSE - t1) / (t1)) ** 2, 12)) ** (1 / 2)


def alpha_128(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha128
100-(100/(1+SUM(((HIGH+LOW+CLOSE)/3>DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUM
E:0),14)/SUM(((HIGH+LOW+CLOSE)/3<DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),
14)))"""
    t1 = (HIGH + LOW + CLOSE) / 3
    t2 = DELAY(t1, 1)
    t3 = t1 * VOLUME
    return 100 - (100 / (1 + SUM(IF(t1 > t2, t3, 0), 14) /
                         SUM(IF(t1 < t2, t3, 0), 14)))


def alpha_129(CLOSE, **kwargs):
    """Alpha129 SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12)"""
    t1 = CLOSE - DELAY(CLOSE, 1)
    return SUM(IF(t1 < 0, ABS(t1), 0), 12)


def alpha_130(HIGH, LOW, VOLUME, VWAP, **kwargs):
    """Alpha130
(RANK(DECAYLINEAR(CORR(((HIGH + LOW) / 2), MEAN(VOLUME,40), 9), 10)) /
RANK(DECAYLINEAR(CORR(RANK(VWAP), RANK(VOLUME), 7),3)))"""
    t1 = CORR(((HIGH + LOW) / 2), MEAN(VOLUME, 40), 9)
    t2 = CORR(RANK(VWAP), RANK(VOLUME), 7)
    return (RANK(DECAYLINEAR(t1, 10)) /
            RANK(DECAYLINEAR(t2, 3)))


def alpha_131(CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha131 (RANK(DELAT(VWAP, 1))^TSRANK(CORR(CLOSE,MEAN(VOLUME,50), 18), 18))"""
    t1 = CORR(CLOSE, MEAN(VOLUME, 50), 18)
    return (RANK(DELTA(VWAP, 1)) ** TSRANK(t1, 18))


def alpha_132(AMOUNT, **kwargs):
    """Alpha132 MEAN(AMOUNT,20)"""
    return MEAN(AMOUNT, 20)


def alpha_133(HIGH, LOW, **kwargs):
    """Alpha133 ((20-HIGHDAY(HIGH,20))/20)*100-((20-LOWDAY(LOW,20))/20)*100"""
    return ((20 - HIGHDAY(HIGH, 20)) / 20) * 100 - ((20 - LOWDAY(LOW, 20)) / 20) * 100


def alpha_134(CLOSE, VOLUME, **kwargs):
    """Alpha134 (CLOSE-DELAY(CLOSE,12))/DELAY(CLOSE,12)*VOLUME"""
    t1 = DELAY(CLOSE, 12)
    return (CLOSE - t1) / t1 * VOLUME


def alpha_135(CLOSE, **kwargs):
    """Alpha135 SMA(DELAY(CLOSE/DELAY(CLOSE,20),1),20,1)"""
    return SMA(DELAY(CLOSE / DELAY(CLOSE, 20), 1), 20, 1)


def alpha_136(OPEN, VOLUME, RET, **kwargs):
    """Alpha136 ((-1 * RANK(DELTA(RET, 3))) * CORR(OPEN, VOLUME, 10))"""
    return ((-1 * RANK(DELTA(RET, 3))) * CORR(OPEN, VOLUME, 10))


def alpha_137(OPEN, HIGH, LOW, CLOSE, **kwargs):
    """Alpha137
16*(CLOSE-DELAY(CLOSE,1)+(CLOSE-OPEN)/2+DELAY(CLOSE,1)-DELAY(OPEN,1))/((ABS(HIGH-DELAY(CLOSE,
1))>ABS(LOW-DELAY(CLOSE,1)) &
ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1))?ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOS
E,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:(ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) &
ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1))?ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLO
SE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OP
EN,1))/4)))*MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1)))"""
    t1 = ABS(HIGH - DELAY(CLOSE, 1))
    t2 = ABS(LOW - DELAY(CLOSE, 1))
    t3 = ABS(HIGH - DELAY(LOW, 1))
    t4 = ABS(DELAY(CLOSE, 1) - DELAY(OPEN, 1))
    t0 = (CLOSE - DELAY(CLOSE, 1) + (CLOSE - OPEN) / 2 + DELAY(CLOSE, 1) - DELAY(OPEN, 1))
    return 16 * t0 / (
        IF((t1 > t2) & (t1 > t3),
           t1 + t2 / 2 + t4 / 4,
           IF((t2 > t3) & (t2 > t1),
              t2 + t1 / 2 + t4 / 4,
              t3 + t4 / 4))) * MAX(t1, t2)


def alpha_138(LOW, VOLUME, VWAP, **kwargs):
    """Alpha138
((RANK(DECAYLINEAR(DELTA((((LOW * 0.7) + (VWAP *0.3))), 3), 20)) -
TSRANK(DECAYLINEAR(TSRANK(CORR(TSRANK(LOW, 8), TSRANK(MEAN(VOLUME,60), 17), 5), 19), 16), 7)) * -1)"""
    t1 = DELTA((((LOW * 0.7) + (VWAP * 0.3))), 3)
    t2 = TSRANK(CORR(TSRANK(LOW, 8), TSRANK(MEAN(VOLUME, 60), 17), 5), 19)
    return ((RANK(DECAYLINEAR(t1, 20)) -
             TSRANK(DECAYLINEAR(t2, 16), 7)) * -1)


def alpha_139(OPEN, VOLUME, **kwargs):
    """Alpha139 (-1 * CORR(OPEN, VOLUME, 10))"""
    return (-1 * CORR(OPEN, VOLUME, 10))


def alpha_140(OPEN, HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha140
MIN(RANK(DECAYLINEAR(((RANK(OPEN) + RANK(LOW)) - (RANK(HIGH) + RANK(CLOSE))), 8)),
TSRANK(DECAYLINEAR(CORR(TSRANK(CLOSE, 8), TSRANK(MEAN(VOLUME,60), 20), 8), 7), 3))"""
    t1 = ((RANK(OPEN) + RANK(LOW)) - (RANK(HIGH) + RANK(CLOSE)))
    t2 = CORR(TSRANK(CLOSE, 8), TSRANK(MEAN(VOLUME, 60), 20), 8)
    return MIN(RANK(DECAYLINEAR(t1, 8)),
               TSRANK(DECAYLINEAR(t2, 7), 3))


def alpha_141(HIGH, VOLUME, **kwargs):
    """Alpha141 (RANK(CORR(RANK(HIGH), RANK(MEAN(VOLUME,15)), 9))* -1)"""
    t1 = CORR(RANK(HIGH), RANK(MEAN(VOLUME, 15)), 9)
    return (RANK(t1) * -1)


def alpha_142(CLOSE, VOLUME, **kwargs):
    """Alpha142
(((-1 * RANK(TSRANK(CLOSE, 10))) * RANK(DELTA(DELTA(CLOSE, 1), 1))) * RANK(TSRANK((VOLUME
/MEAN(VOLUME,20)), 5)))"""
    t1 = TSRANK(CLOSE, 10)
    t2 = DELTA(DELTA(CLOSE, 1), 1)
    t3 = TSRANK((VOLUME / MEAN(VOLUME, 20)), 5)
    return (((-1 * RANK(t1)) * RANK(t2)) * RANK(t3))


def alpha_143(CLOSE, **kwargs):
    """Alpha143 CLOSE>DELAY(CLOSE,1)?(CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*SELF:SELF"""
    t1 = DELAY(CLOSE, 1)
    t2 = IF(CLOSE > t1, CLOSE / t1 - 1., 1.)
    return CUMPROD(t2)


def alpha_144(CLOSE, AMOUNT, **kwargs):
    """Alpha144
SUMIF(ABS(CLOSE/DELAY(CLOSE,1)-1)/AMOUNT,20,CLOSE<DELAY(CLOSE,1))/COUNT(CLOSE<DELAY(CLOSE,
1),20)"""
    t1 = DELAY(CLOSE, 1)
    t2 = CLOSE < t1
    return SUMIF(ABS(CLOSE / t1 - 1) / AMOUNT,
                 t2,
                 20) / COUNT(t2, 20)


def alpha_145(VOLUME, **kwargs):
    """Alpha145 (MEAN(VOLUME,9)-MEAN(VOLUME,26))/MEAN(VOLUME,12)*100"""
    return (MEAN(VOLUME, 9) - MEAN(VOLUME, 26)) / MEAN(VOLUME, 12) * 100


def alpha_146(CLOSE, **kwargs):
    """Alpha146
MEAN((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)-SMA((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1),61,2),20)*((
CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)-SMA((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1),61,2))/SMA(((CLOS
E-DELAY(CLOSE,1))/DELAY(CLOSE,1)-((CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)-SMA((CLOSE-DELAY(CLOSE,
1))/DELAY(CLOSE,1),61,2)))^2,60);"""
    """TODO: 这也有问题"""
    t0 = DELAY(CLOSE, 1)
    t1 = (CLOSE - t0) / t0
    t2 = SMA(t1, 61, 2)
    t3 = t1 - t2
    return MEAN(t3, 20) * t3 / SMA(t2 ** 2, 60, 1)


def alpha_147(CLOSE, **kwargs):
    """Alpha147 REGBETA(MEAN(CLOSE,12),SEQUENCE(12))"""
    return REGSLOPE(MEAN(CLOSE, 12), 12)


def alpha_148(OPEN, VOLUME, **kwargs):
    """Alpha148 ((RANK(CORR((OPEN), SUM(MEAN(VOLUME,60), 9), 6)) < RANK((OPEN - TSMIN(OPEN, 14)))) * -1)"""
    t1 = CORR((OPEN), SUM(MEAN(VOLUME, 60), 9), 6)
    t2 = (OPEN - TSMIN(OPEN, 14))
    return (LessThan(RANK(t1),
                     RANK(t2)) * -1)


def alpha_149(CLOSE, BANCHMARKINDEXCLOSE, **kwargs):
    """Alpha149
REGBETA(FILTER(CLOSE/DELAY(CLOSE,1)-1,BANCHMARKINDEXCLOSE<DELAY(BANCHMARKINDEXCLOSE,1)
),FILTER(BANCHMARKINDEXCLOSE/DELAY(BANCHMARKINDEXCLOSE,1)-1,BANCHMARKINDEXCLOSE<DELA
Y(BANCHMARKINDEXCLOSE,1)),252)"""
    t1 = DELAY(CLOSE, 1)
    t2 = DELAY(BANCHMARKINDEXCLOSE, 1)
    return REGBETA(FILTER(CLOSE / t1 - 1,
                          BANCHMARKINDEXCLOSE < t2),
                   FILTER(BANCHMARKINDEXCLOSE / t2 - 1,
                          BANCHMARKINDEXCLOSE < t2), 252)


def alpha_150(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha150 (CLOSE+HIGH+LOW)/3*VOLUME"""
    return (CLOSE + HIGH + LOW) / 3 * VOLUME


def alpha_151(CLOSE, **kwargs):
    """Alpha151 SMA(CLOSE-DELAY(CLOSE,20),20,1)"""
    return SMA(CLOSE - DELAY(CLOSE, 20), 20, 1)


def alpha_152(CLOSE, **kwargs):
    """Alpha152
SMA(MEAN(DELAY(SMA(DELAY(CLOSE/DELAY(CLOSE,9),1),9,1),1),12)-MEAN(DELAY(SMA(DELAY(CLOSE/DELAY
(CLOSE,9),1),9,1),1),26),9,1)"""
    t1 = DELAY(SMA(DELAY(CLOSE / DELAY(CLOSE, 9), 1), 9, 1), 1)
    return SMA(MEAN(t1, 12) -
               MEAN(t1, 26), 9, 1)


def alpha_153(CLOSE, **kwargs):
    """Alpha153 (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/4"""
    return (MEAN(CLOSE, 3) + MEAN(CLOSE, 6) + MEAN(CLOSE, 12) + MEAN(CLOSE, 24)) / 4


def alpha_154(VOLUME, VWAP, **kwargs):
    """Alpha154 (((VWAP - MIN(VWAP, 16))) < (CORR(VWAP, MEAN(VOLUME,180), 18)))"""
    t1 = ((VWAP - MIN(VWAP, 16)))
    t2 = (CORR(VWAP, MEAN(VOLUME, 180), 18))
    return LessThan(t1, t2)


def alpha_155(VOLUME, **kwargs):
    """Alpha155 SMA(VOLUME,13,2)-SMA(VOLUME,27,2)-SMA(SMA(VOLUME,13,2)-SMA(VOLUME,27,2),10,2)"""
    t1 = SMA(VOLUME, 13, 2) - SMA(VOLUME, 27, 2)
    return t1 - SMA(t1, 10, 2)


def alpha_156(OPEN, LOW, VWAP, **kwargs):
    """Alpha156
(MAX(RANK(DECAYLINEAR(DELTA(VWAP, 5), 3)), RANK(DECAYLINEAR(((DELTA(((OPEN * 0.15) + (LOW *0.85)),
2) / ((OPEN * 0.15) + (LOW * 0.85))) * -1), 3))) * -1)"""
    t1 = ((OPEN * 0.15) + (LOW * 0.85))
    t2 = DELTA(VWAP, 5)
    t3 = ((DELTA(t1, 2) / t1) * -1)
    return (MAX(RANK(DECAYLINEAR(t2, 3)),
                RANK(DECAYLINEAR(t3, 3))) * -1)


def alpha_157(CLOSE, RET, **kwargs):
    """Alpha157
(MIN(PROD(RANK(RANK(LOG(SUM(TSMIN(RANK(RANK((-1 * RANK(DELTA((CLOSE - 1), 5))))), 2), 1)))), 1), 5) +
TSRANK(DELAY((-1 * RET), 6), 5))"""
    return (MIN(RANK(LOG(SUM(TSMIN(RANK((-1 * RANK(DELTA((CLOSE - 1), 5)))), 2), 1))), 5) +
            TSRANK(DELAY((-1 * RET), 6), 5))


def alpha_158(HIGH, LOW, CLOSE, **kwargs):
    """Alpha158 ((HIGH-SMA(CLOSE,15,2))-(LOW-SMA(CLOSE,15,2)))/CLOSE"""
    t1 = SMA(CLOSE, 15, 2)
    return ((HIGH - t1) - (LOW - t1)) / CLOSE


def alpha_159(HIGH, LOW, CLOSE, **kwargs):
    """Alpha159
((CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),6))/SUM(MAX(HGIH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),6)
*12*24+(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),12))/SUM(MAX(HGIH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CL
OSE,1)),12)*6*24+(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),24))/SUM(MAX(HGIH,DELAY(CLOSE,1))-MIN(LOW,D
ELAY(CLOSE,1)),24)*6*24)*100/(6*12+6*24+12*24)"""
    t1 = MIN(LOW, DELAY(CLOSE, 1))
    t2 = MAX(HIGH, DELAY(CLOSE, 1))
    t3 = t2 - t1
    return ((CLOSE - SUM(t1, 6)) / SUM(t3, 6) * 12 * 24 +
            (CLOSE - SUM(t1, 12)) / SUM(t3, 12) * 6 * 24 +
            (CLOSE - SUM(t1, 24)) / SUM(t3, 24) * 6 * 24) * 100 / (6 * 12 + 6 * 24 + 12 * 24)


def alpha_160(CLOSE, **kwargs):
    """Alpha160 SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)"""
    return SMA(IF(CLOSE <= DELAY(CLOSE, 1), STD(CLOSE, 20), 0), 20, 1)


def alpha_161(HIGH, LOW, CLOSE, **kwargs):
    """Alpha161 MEAN(MAX(MAX((HIGH-LOW),ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),12)"""
    # ATR?
    t1 = DELAY(CLOSE, 1)
    return MEAN(MAX(MAX((HIGH - LOW), ABS(t1 - HIGH)), ABS(t1 - LOW)), 12)


def alpha_162(CLOSE, **kwargs):
    """Alpha162
(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100-MIN(SMA(MAX(CLOS
E-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))/(MAX(SMA(MAX(CLOSE-DELAY(C
LOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12)-MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,
1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))"""
    t0 = CLOSE - DELAY(CLOSE, 1)
    t1 = SMA(MAX(t0, 0), 12, 1) / SMA(ABS(t0), 12, 1) * 100
    t2 = MIN(t1, 12)
    t3 = MAX(t1, 12)
    return (t1 - t2) / (t3 - t2)


def alpha_163(HIGH, CLOSE, VOLUME, VWAP, RET, **kwargs):
    """Alpha163 RANK(((((-1 * RET) * MEAN(VOLUME,20)) * VWAP) * (HIGH - CLOSE)))"""
    return RANK(((((-1 * RET) * MEAN(VOLUME, 20)) * VWAP) * (HIGH - CLOSE)))


def alpha_164(HIGH, LOW, CLOSE, **kwargs):
    """Alpha164
SMA((((CLOSE>DELAY(CLOSE,1))?1/(CLOSE-DELAY(CLOSE,1)):1)-MIN(((CLOSE>DELAY(CLOSE,1))?1/(CLOSE-D
ELAY(CLOSE,1)):1),12))/(HIGH-LOW)*100,13,2)"""
    t0 = DELAY(CLOSE, 1)
    t1 = IF((CLOSE > t0), 1 / (CLOSE - t0), 1)
    return SMA((t1 - MIN(t1, 12)) / (HIGH - LOW) * 100, 13, 2)


def alpha_165(CLOSE, **kwargs):
    """Alpha165 MAX(SUMAC(CLOSE-MEAN(CLOSE,48)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,48)))/STD(CLOSE,48)"""
    # return MAX(SUMAC(CLOSE - MEAN(CLOSE, 48))) - MIN(SUMAC(CLOSE - MEAN(CLOSE, 48))) / STD(CLOSE, 48)
    pass


def alpha_166(CLOSE, **kwargs):
    """Alpha166
-20*(20-1)
^1.5*SUM(CLOSE/DELAY(CLOSE,1)-1-MEAN(CLOSE/DELAY(CLOSE,1)-1,20),20)/((20-1)*(20-2)(SUM((CLOSE/DELA
Y(CLOSE,1),20)^2,20))^1.5)
"""
    t1 = CLOSE / DELAY(CLOSE, 1)
    return -20 * (20 - 1) ** 1.5 * SUM(t1 - 1 - MEAN(t1 - 1, 20), 20) / (
            (20 - 1) * (20 - 2) * (SUM(t1 ** 2, 20)) ** 1.5)


def alpha_167(CLOSE, **kwargs):
    """Alpha167 SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)"""
    t1 = DELAY(CLOSE, 1)
    return SUM(IF(CLOSE - t1 > 0, CLOSE - t1, 0), 12)


def alpha_168(VOLUME, **kwargs):
    """Alpha168 (-1*VOLUME/MEAN(VOLUME,20))"""
    return (-1 * VOLUME / MEAN(VOLUME, 20))


def alpha_169(CLOSE, **kwargs):
    """Alpha169
SMA(MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),12)-MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),
26),10,1)"""
    t1 = DELAY(SMA(CLOSE - DELAY(CLOSE, 1), 9, 1), 1)
    return SMA(MEAN(t1, 12) -
               MEAN(t1, 26), 10, 1)


def alpha_170(HIGH, CLOSE, VOLUME, VWAP, **kwargs):
    """Alpha170
((((RANK((1 / CLOSE)) * VOLUME) / MEAN(VOLUME,20)) * ((HIGH * RANK((HIGH - CLOSE))) / (SUM(HIGH, 5) /
5))) - RANK((VWAP - DELAY(VWAP, 5))))"""
    return ((((RANK((1 / CLOSE)) * VOLUME) / MEAN(VOLUME, 20)) * (
            (HIGH * RANK((HIGH - CLOSE))) / (SUM(HIGH, 5) / 5))) - RANK((VWAP - DELAY(VWAP, 5))))


def alpha_171(OPEN, HIGH, LOW, CLOSE, **kwargs):
    """Alpha171 ((-1 * ((LOW - CLOSE) * (OPEN^5))) / ((CLOSE - HIGH) * (CLOSE^5)))"""
    return ((-1 * ((LOW - CLOSE) * (OPEN ** 5))) / ((CLOSE - HIGH) * (CLOSE ** 5)))


def alpha_172(HIGH, LOW, CLOSE, **kwargs):
    """Alpha172
MEAN(ABS(SUM((LD>0 & LD>HD)?LD:0,14)*100/SUM(TR,14)-SUM((HD>0 &
HD>LD)?HD:0,14)*100/SUM(TR,14))/(SUM((LD>0 & LD>HD)?LD:0,14)*100/SUM(TR,14)+SUM((HD>0 &
HD>LD)?HD:0,14)*100/SUM(TR,14))*100,6)"""
    TR = MAX(MAX(HIGH - LOW, ABS(HIGH - DELAY(CLOSE, 1))), ABS(LOW - DELAY(CLOSE, 1)))
    HD = HIGH - DELAY(HIGH, 1)
    LD = DELAY(LOW, 1) - LOW

    t1 = SUM(TR, 14)
    t2 = SUM(IF(((LD > 0) & (LD > HD)), LD, 0), 14) * 100 / t1
    t3 = SUM(IF(((HD > 0) & (HD > LD)), HD, 0), 14) * 100 / t1

    return MEAN(ABS(t2 - t3) / (t2 + t3) * 100, 6)


def alpha_173(CLOSE, **kwargs):
    """Alpha173 3*SMA(CLOSE,13,2)-2*SMA(SMA(CLOSE,13,2),13,2)+SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2);"""
    t1 = SMA(CLOSE, 13, 2)
    t2 = SMA(LOG(CLOSE), 13, 2)
    return 3 * t1 - 2 * SMA(t1, 13, 2) + SMA(SMA(t2, 13, 2), 13, 2)


def alpha_174(CLOSE, **kwargs):
    """Alpha174 SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)"""
    return SMA(IF(CLOSE > DELAY(CLOSE, 1), STD(CLOSE, 20), 0), 20, 1)


def alpha_175(HIGH, LOW, CLOSE, **kwargs):
    """Alpha175 MEAN(MAX(MAX((HIGH-LOW),ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),6)"""
    t1 = DELAY(CLOSE, 1)
    return MEAN(MAX(MAX((HIGH - LOW), ABS(t1 - HIGH)), ABS(t1 - LOW)), 6)


def alpha_176(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """Alpha176 CORR(RANK(((CLOSE - TSMIN(LOW, 12)) / (TSMAX(HIGH, 12) - TSMIN(LOW,12)))), RANK(VOLUME), 6)"""
    x1 = TSMAX(HIGH, 12)
    x2 = TSMIN(LOW, 12)
    t1 = ((CLOSE - x2) / (x1 - x2))
    return CORR(RANK(t1), RANK(VOLUME), 6)


def alpha_177(HIGH, **kwargs):
    """Alpha177 ((20-HIGHDAY(HIGH,20))/20)*100"""
    return ((20 - HIGHDAY(HIGH, 20)) / 20) * 100


def alpha_178(CLOSE, VOLUME, **kwargs):
    """Alpha178 (CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*VOLUME"""
    t1 = DELAY(CLOSE, 1)
    return (CLOSE - t1) / t1 * VOLUME


def alpha_179(LOW, VOLUME, VWAP, **kwargs):
    """Alpha179 (RANK(CORR(VWAP, VOLUME, 4)) *RANK(CORR(RANK(LOW), RANK(MEAN(VOLUME,50)), 12)))"""
    t1 = CORR(VWAP, VOLUME, 4)
    t2 = CORR(RANK(LOW), RANK(MEAN(VOLUME, 50)), 12)
    return (RANK(t1) * RANK(t2))


def alpha_180(CLOSE, VOLUME, **kwargs):
    """Alpha180
((MEAN(VOLUME,20) < VOLUME) ? ((-1 * TSRANK(ABS(DELTA(CLOSE, 7)), 60)) * SIGN(DELTA(CLOSE, 7)) : (-1 *
VOLUME)))"""
    t1 = DELTA(CLOSE, 7)
    return IF((MEAN(VOLUME, 20) < VOLUME),
              (-1 * TSRANK(ABS(t1), 60)) * SIGN(t1),
              (-1 * VOLUME))


def alpha_181(CLOSE, BANCHMARKINDEXCLOSE, **kwargs):
    """Alpha181
SUM(((CLOSE/DELAY(CLOSE,1)-1)-MEAN((CLOSE/DELAY(CLOSE,1)-1),20))-(BANCHMARKINDEXCLOSE-MEAN(B
ANCHMARKINDEXCLOSE,20))^2,20)/SUM((BANCHMARKINDEXCLOSE-MEAN(BANCHMARKINDEXCLOSE,20))^3)"""
    """!!!又补了一个参数20"""
    t1 = (CLOSE / DELAY(CLOSE, 1) - 1)
    t2 = (BANCHMARKINDEXCLOSE - MEAN(BANCHMARKINDEXCLOSE, 20))
    return SUM((t1 - MEAN(t1, 20)) - (t2) ** 2, 20) / SUM(t2 ** 3, 20)


def alpha_182(OPEN, CLOSE, BANCHMARKINDEXCLOSE, BANCHMARKINDEXOPEN, **kwargs):
    """Alpha182
COUNT((CLOSE>OPEN & BANCHMARKINDEXCLOSE>BANCHMARKINDEXOPEN)OR(CLOSE<OPEN &
BANCHMARKINDEXCLOSE<BANCHMARKINDEXOPEN),20)/20"""
    t1 = ((CLOSE > OPEN) & (BANCHMARKINDEXCLOSE > BANCHMARKINDEXOPEN))
    t2 = ((CLOSE < OPEN) & (BANCHMARKINDEXCLOSE < BANCHMARKINDEXOPEN))
    return COUNT(t1 | t2, 20) / 20


def alpha_183(CLOSE, **kwargs):
    """Alpha183 MAX(SUMAC(CLOSE-MEAN(CLOSE,24)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,24)))/STD(CLOSE,24)"""
    pass
    # return MAX(SUMAC(CLOSE-MEAN(CLOSE,24)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,24)))/STD(CLOSE,24)


def alpha_184(OPEN, CLOSE, **kwargs):
    """Alpha184 (RANK(CORR(DELAY((OPEN - CLOSE), 1), CLOSE, 200)) + RANK((OPEN - CLOSE)))"""
    t0 = (OPEN - CLOSE)
    t1 = CORR(DELAY(t0, 1), CLOSE, 200)
    return (RANK(t1) + RANK(t0))


def alpha_185(OPEN, CLOSE, **kwargs):
    """Alpha185 RANK((-1 * ((1 - (OPEN / CLOSE))^2)))"""
    return RANK((-1 * ((1 - (OPEN / CLOSE)) ** 2)))


def alpha_186(HIGH, LOW, CLOSE, **kwargs):
    """Alpha186
(MEAN(ABS(SUM((LD>0 & LD>HD)?LD:0,14)*100/SUM(TR,14)-SUM((HD>0 &
HD>LD)?HD:0,14)*100/SUM(TR,14))/(SUM((LD>0 & LD>HD)?LD:0,14)*100/SUM(TR,14)+SUM((HD>0 &
HD>LD)?HD:0,14)*100/SUM(TR,14))*100,6)+DELAY(MEAN(ABS(SUM((LD>0 &
LD>HD)?LD:0,14)*100/SUM(TR,14)-SUM((HD>0 & HD>LD)?HD:0,14)*100/SUM(TR,14))/(SUM((LD>0 &
LD>HD)?LD:0,14)*100/SUM(TR,14)+SUM((HD>0 & HD>LD)?HD:0,14)*100/SUM(TR,14))*100,6),6))/2"""

    TR = MAX(MAX(HIGH - LOW, ABS(HIGH - DELAY(CLOSE, 1))), ABS(LOW - DELAY(CLOSE, 1)))
    HD = HIGH - DELAY(HIGH, 1)
    LD = DELAY(LOW, 1) - LOW

    t1 = SUM(TR, 14)
    t2 = SUM(IF(((LD > 0) & (LD > HD)), LD, 0), 14) * 100 / t1
    t3 = SUM(IF(((HD > 0) & (HD > LD)), HD, 0), 14) * 100 / t1

    t4 = MEAN(ABS(t2 - t3) / (t2 + t3) * 100, 6)
    return (t4 + DELAY(t4, 6)) / 2


def alpha_187(OPEN, HIGH, **kwargs):
    """Alpha187 SUM((OPEN<=DELAY(OPEN,1)?0:MAX((HIGH-OPEN),(OPEN-DELAY(OPEN,1)))),20)"""
    t1 = DELAY(OPEN, 1)
    return SUM(IF(OPEN <= t1, 0, MAX((HIGH - OPEN), (OPEN - t1))), 20)


def alpha_188(HIGH, LOW, **kwargs):
    """Alpha188 ((HIGH-LOW–SMA(HIGH-LOW,11,2))/SMA(HIGH-LOW,11,2))*100"""
    t0 = HIGH - LOW
    t1 = SMA(t0, 11, 2)
    return ((t0 - t1) / t1) * 100


def alpha_189(CLOSE, **kwargs):
    """Alpha189 MEAN(ABS(CLOSE-MEAN(CLOSE,6)),6)"""
    return MEAN(ABS(CLOSE - MEAN(CLOSE, 6)), 6)


def alpha_190(CLOSE, **kwargs):
    """Alpha190
LOG((COUNT(CLOSE/DELAY(CLOSE)-1>((CLOSE/DELAY(CLOSE,19))^(1/20)-1),20)-1)*(SUMIF(((CLOSE/DELAY(C
LOSE)-1-(CLOSE/DELAY(CLOSE,19))^(1/20)-1))^2,20,CLOSE/DELAY(CLOSE)-1<(CLOSE/DELAY(CLOSE,19))^(1/20)-
1))/((COUNT((CLOSE/DELAY(CLOSE)-1<(CLOSE/DELAY(CLOSE,19))^(1/20)-1),20))*(SUMIF((CLOSE/DELAY(CLOS
E)-1-((CLOSE/DELAY(CLOSE,19))^(1/20)-1))^2,20,CLOSE/DELAY(CLOSE)-1>(CLOSE/DELAY(CLOSE,19))^(1/20)-1)))
)"""
    t1 = CLOSE / DELAY(CLOSE, 1) - 1
    t2 = (CLOSE / DELAY(CLOSE, 19)) ** (1 / 20) - 1
    t3 = (t1 - t2) ** 2
    t4 = t1 > t2
    t5 = t1 < t2
    return LOG((COUNT(t4, 20)) * (SUMIF(t3, t5, 20)) /
               ((COUNT(t5, 20)) * (SUMIF(t3, t4, 20))))


def alpha_191(HIGH, LOW, CLOSE, VOLUME, **kwargs):
    """((CORR(MEAN(VOLUME,20), LOW, 5) + ((HIGH + LOW) / 2)) - CLOSE)"""
    return ((CORR(MEAN(VOLUME, 20), LOW, 5) + ((HIGH + LOW) / 2)) - CLOSE)
