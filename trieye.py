#coding=utf-8
import sys, gevent,datetime
from btc.btcchina import BTCChina
BTCCHINA_ACCESS_KEY = ''
BTCCHINA_SECRET_KEY = ''

b = BTCChina(BTCCHINA_ACCESS_KEY, BTCCHINA_SECRET_KEY, 5)
markets = ['btccny', 'ltccny', 'btcltc']
jobs = []

for m in markets:
    j = gevent.spawn(b.get_depth2, m)
    jobs.append(j)
gevent.joinall(jobs)

depths = []
for j in jobs:
    d = j.value
    if not d:
        print 'Get depths fails.'
        sys.exit(2)
    
    i = jobs.index(j)
    m = markets[i]
    print '\n%s depth:'%m
    print 'sell:'
    for a in d['asks'][-5:]:
        print a[0], a[1]
    print 'buy:'
    for b in d['bids'][:5]:
        print b[0], b[1]
    depths.append(d)

print '\npath: cny->btc->ltc->cny'
print 'cny->btc:', depths[0]['asks'][-1]
s1 = depths[0]['asks'][-1]
print 'btc->ltc:', depths[2]['asks'][-1]
s2 = depths[2]['asks'][-1]
print 'ltc->cny:', depths[1]['bids'][0]
s3 = depths[1]['bids'][0]

ltc_amount = min(float(s2[1]), float(s3[1]))
print 'ltc amount:%s'%str(ltc_amount)

btc_amount = min([float(s1[1]), float(s2[0])*ltc_amount])
print 'btc amount:%s'%str(btc_amount)

print 'cny->btc: use %s cny buy %s btc.'%(str(float(s1[0]) * btc_amount), str(btc_amount))
print 'btc->ltc: use %s btc buy %s ltc.'%(str(btc_amount), str(btc_amount/float(s2[0])) )
print 'ltc->cny: sell %s ltc get %s cny.'%(str(btc_amount/float(s2[0])), str(btc_amount /float(s2[0]) * float(s3[0])) )
profit = btc_amount /float(s2[0]) * float(s3[0]) - float(s1[0]) * btc_amount
volumn = float(s1[0]) * btc_amount
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
if profit > 0:
    print '%s: path: cny->btc->ltc->cny; profit(+) %s, volumn:%s cny'%(now, str(profit), str(volumn))
else:
    print '%s: path: cny->btc->ltc->cny; profit %s, volumn:%s cny'%(now, str(profit), str(volumn))

print '\npath: cny->ltc->btc->cny'
print 'cny->ltc:', depths[1]['asks'][-1]
s1 = depths[1]['asks'][-1]
print 'ltc->btc', depths[2]['bids'][0]
s2 = depths[2]['bids'][0]
print 'btc->cny', depths[0]['bids'][0]
s3 = depths[0]['bids'][0]

btc_amount = min(float(s3[1]),float(s2[0])*float(s2[1]))
print 'btc_amount:%s'%str(btc_amount)

ltc_amount = min(float(s1[1]), btc_amount/float(s2[0]))
print 'ltc_amount:%s'%str(ltc_amount)

print 'cny->ltc: use %s cny buy %s ltc'%(str(float(s1[0])*ltc_amount), str(ltc_amount))
print 'ltc->btc: sell %s ltc, get %s btc'%(str(ltc_amount), str(ltc_amount*float(s2[0])))
print 'btc->cny: sell %s btc, get %s cny'%(str(ltc_amount*float(s2[0])), str(ltc_amount*float(s2[0])*float(s3[0])))
profit = ltc_amount*float(s2[0])*float(s3[0]) - float(s1[0])*ltc_amount
volumn = float(s1[0])*ltc_amount
if profit > 0:
    print '%s: path: cny->ltc->btc->cny; profit(+) %s, volumne: %s cny'%(now, str(profit), str(volumn))
else:
    print '%s: path: cny->ltc->btc->cny; profit %s, volumne: %s cny'%(now, str(profit), str(volumn))
