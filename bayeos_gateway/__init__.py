from bayeos_gateway.bayeosGatewayClient import BayEOSWriter, BayEOSSender, BayEOS

def main():
    bayeos = BayEOS()
    
    dataFrame = BayEOS.createDataFrame(bayeos, [[0,2], [1,3], [3,20]], 0x01, 1)
    print(BayEOS.parseFrame(bayeos, dataFrame))
    
main()    
    