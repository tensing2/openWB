#!/usr/bin/python3
from typing import List
import os, sys, traceback, time
try: # make script callable from command line and LRS
    from bezug_rct2 import rct_lib
except:
    import rct_lib

# Author Heinz Hoefling
# Version 1.0 Okt.2021
# Fragt die Werte gebuendelt ab, nicht mit einer Connection je Wert

# Entry point with parameter check
def main(argv: List[str]):
    start_time = time.time()
    rct = rct_lib.RCT(argv)

    if rct.connect_to_server() == True:
        try:
            # generate id list for fast bulk read
            MyTab = []
            totalfeed   = rct.add_by_name(MyTab, 'energy.e_grid_feed_total')
            totalload   = rct.add_by_name(MyTab, 'energy.e_grid_load_total')
            p_ac_sc_sum = rct.add_by_name(MyTab, 'g_sync.p_ac_sc_sum')
            volt1       = rct.add_by_name(MyTab, 'g_sync.u_l_rms[0]')
            volt2       = rct.add_by_name(MyTab, 'g_sync.u_l_rms[1]')
            volt3       = rct.add_by_name(MyTab, 'g_sync.u_l_rms[2]')
            watt1       = rct.add_by_name(MyTab, 'g_sync.p_ac_sc[0]')
            watt2       = rct.add_by_name(MyTab, 'g_sync.p_ac_sc[1]')
            watt3       = rct.add_by_name(MyTab, 'g_sync.p_ac_sc[2]')
            freq        = rct.add_by_name(MyTab, 'grid_pll[0].f')
            stat1       = rct.add_by_name(MyTab, 'fault[0].flt')
            stat2       = rct.add_by_name(MyTab, 'fault[1].flt')
            stat3       = rct.add_by_name(MyTab, 'fault[2].flt')
            stat4       = rct.add_by_name(MyTab, 'fault[3].flt')                        
            
            #Speicher
            socx    = rct.add_by_name(MyTab, 'battery.soc')
            bwatt1   = rct.add_by_name(MyTab, 'g_sync.p_acc_lp')
            bwatt2   = rct.add_by_name(MyTab, 'battery.stored_energy')
            bwatt3   = rct.add_by_name(MyTab, 'battery.used_energy')
            bstat1  = rct.add_by_name(MyTab, 'battery.bat_status')
            bstat2  = rct.add_by_name(MyTab, 'battery.status')
            bstat3  = rct.add_by_name(MyTab, 'battery.status2')
            socsoll = rct.add_by_name(MyTab, 'battery.soc_target')
            
            #WR
            pv1watt  = rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].p_dc')
            pv2watt  = rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].p_dc')
            pv3watt  = rct.add_by_name(MyTab, 'io_board.s0_external_power')
            pLimit   = rct.add_by_name(MyTab, 'p_rec_lim[2]')   # max. AC power according to RCT Power
            dA       = rct.add_by_name(MyTab, 'energy.e_dc_day[0]')
            dB       = rct.add_by_name(MyTab, 'energy.e_dc_day[1]')
            dE       = rct.add_by_name(MyTab, 'energy.e_ext_day')
            mA       = rct.add_by_name(MyTab, 'energy.e_dc_month[0]')
            mB       = rct.add_by_name(MyTab, 'energy.e_dc_month[1]')
            mE       = rct.add_by_name(MyTab, 'energy.e_ext_month')
            yA       = rct.add_by_name(MyTab, 'energy.e_dc_year[0]')
            yB       = rct.add_by_name(MyTab, 'energy.e_dc_year[1]')
            yE       = rct.add_by_name(MyTab, 'energy.e_ext_year')
            pv1total = rct.add_by_name(MyTab, 'energy.e_dc_total[0]')
            pv2total = rct.add_by_name(MyTab, 'energy.e_dc_total[1]')
            pv3total = rct.add_by_name(MyTab, 'energy.e_ext_total')            
            
            #Ralf
            hausEnergy   = rct.add_by_name(MyTab, 'energy.e_load_total')
            hausWatt1    = rct.add_by_name(MyTab, 'g_sync.p_ac_load[0]')
            hausWatt2    = rct.add_by_name(MyTab, 'g_sync.p_ac_load[1]')
            hausWatt3    = rct.add_by_name(MyTab, 'g_sync.p_ac_load[2]')            

            # read all parameters
            response = rct.read(MyTab)
            rct.close()
            
            # postprocess values Bezug
            totalfeed   = int(totalfeed.value*-1.0)
            totalload   = int(totalload.value)
            p_ac_sc_sum = p_ac_sc_sum.value
            volt1       = int(volt1.value * 10) / 10.0
            volt2       = int(volt2.value * 10) / 10.0
            volt3       = int(volt3.value * 10) / 10.0
            watt1       = int(watt1.value)
            watt2       = int(watt2.value)
            watt3       = int(watt3.value)
            freq        = int(freq.value * 100) / 100.0
            stat1       = int(stat1.value)
            stat2       = int(stat2.value)
            stat3       = int(stat3.value)
            stat4       = int(stat4.value)            
            
            # postprocess values Speicher
            socx    = socx.value
            soc = int(socx * 100.0)
            bwatt1  = int(bwatt1.value) * -1.0
            bwatt2  = int(bwatt2.value)
            bwatt3  = int(bwatt3.value)
            bstat1  = int(bstat1.value)
            bstat2  = int(bstat2.value)
            bstat3  = int(bstat3.value)
            socsoll = int(socsoll.value * 100.0)
            
            # postprocess values WR
            # actual DC power
            rct.write_ramdisk('pv1wattString1', pv1watt.value, 'pv1watt')
            rct.write_ramdisk('pv1wattString2', pv2watt.value, 'pv2watt')
            pvwatt = pv1watt.value + pv2watt.value + pv3watt.value
            rct.write_ramdisk('pvwatt', int(pvwatt) * -1, 'negative Summe von pv1watt + pv2watt + pv3watt')

            # max. possible AC power (might be used by the control loop to limit PV charging power)
            rct.write_ramdisk('maxACkW', int(pLimit.value), 'Maximale zur Ladung verwendete AC-Leistung des Wechselrichters')

            # daily
            daily_pvkwhk = (dA.value + dB.value + dE.value) / 1000.0   # -> KW
            rct.write_ramdisk('daily_pvkwhk', daily_pvkwhk, 'daily_pvkwhk')

            # monthly
            monthly_pvkwhk = (mA.value + mB.value + mE.value) / 1000.0   # -> KW
            rct.write_ramdisk('monthly_pvkwhk', monthly_pvkwhk, 'monthly_pvkwhk')

            # yearly
            yearly_pvkwhk = (yA.value + yB.value + yE.value) / 1000.0   # -> KW
            rct.write_ramdisk('yearly_pvkwhk', yearly_pvkwhk, 'yearly_pvkwhk')

            # total
            pvkwh = (pv1total.value + pv2total.value + pv3total.value)
            rct.write_ramdisk('pvkwh', pvkwh, 'Summe von pv1total pv1total pv1total')
            
            
            
            # postprocess values Ralf
            hausEnergy  = int(hausEnergy.value)
            hausWatt1   = int(hausWatt1.value)
            hausWatt2   = int(hausWatt2.value)
            hausWatt3   = int(hausWatt3.value)

            #
            # Adjust and write values to ramdisk bezug
            rct.write_ramdisk('einspeisungkwh', totalfeed, '0x44D4C533 energy.e_grid_feed_total')
            rct.write_ramdisk('bezugkwh',       totalload, '#0x62FBE7DC energy.e_grid_load_total')
            rct.write_ramdisk('wattbezug', int(p_ac_sc_sum)*1, '#0x6002891F g_sync.p_ac_sc_sum')
            rct.write_ramdisk('evuv1', volt1, '0xCF053085 g_sync.u_l_rms[0] ')
            rct.write_ramdisk('evuv2', volt2, '0x54B4684E g_sync.u_l_rms[1] ')
            rct.write_ramdisk('evuv3', volt3, '0x2545E22D g_sync.u_l_rms[2] ')

            rct.write_ramdisk('bezugw1', watt1, '0x27BE51D9 als Watt g_sync.p_ac_sc[0]')
            ampere = int(watt1 / volt1 * 10.0) / 10.0
            rct.write_ramdisk('bezuga1', ampere, '0x27BE51D9 als Ampere g_sync.p_ac_sc[0]')

            rct.write_ramdisk('bezugw2', watt2, '0xF5584F90 als Watt g_sync.p_ac_sc[1]')
            ampere = int(watt2 / volt2 * 10.0) / 10.0
            rct.write_ramdisk('bezuga2', ampere, '0xF5584F90 als Ampere g_sync.p_ac_sc[1]')

            rct.write_ramdisk('bezugw3', watt3, '0xB221BCFA als Watt g_sync.p_ac_sc[2]')
            ampere = int(watt3 / volt3 * 10.0) / 10.0
            rct.write_ramdisk('bezuga3', ampere, '0xF5584F90 als Ampere g_sync.p_ac_sc[2]')

            rct.write_ramdisk('evuhz', freq, '0x1C4A665F grid_pll[0].f')
            rct.write_ramdisk('llhz', freq, '0x1C4A665F grid_pll[0].f')                                    
            
            # Adjust and write values to ramdisk Speicher
            rct.write_ramdisk('speichersoc', soc, '0x959930BF battery.soc')
            rct.write_ramdisk('speicherleistung', bwatt1, '0x400F015B g_sync.p_acc_lp')
            rct.write_ramdisk('speicherikwh', bwatt2, '0x5570401B battery.stored_energy')
            rct.write_ramdisk('speicherekwh', bwatt3, '#0xA9033880 battery.used_energy')
            
            
            #Ralf
            rct.write_ramdisk('hausEnergy', hausEnergy, '0xEFF4B537 energy.e_load_total')
            rct.write_ramdisk('hausWatt1', hausWatt1, '0x03A39CA2 g_sync.p_ac_load[0]')
            rct.write_ramdisk('hausWatt2', hausWatt2, '0x2788928C g_sync.p_ac_load[1]')
            rct.write_ramdisk('hausWatt3', hausWatt3, '0xF0B436DD g_sync.p_ac_load[2]')
            
            verluste = pvwatt - bwatt1 - hausWatt1 - hausWatt2 - hausWatt3
            verluste = int(verluste)
            
            rct.write_ramdisk('hausVerluste', verluste, 'Hausverluste')            
            os.system('mosquitto_pub -r -t openWB/SmartHome/set/Devices/2/Aktpower -m "' + str(verluste) + '"')         
            
            
            # process Errors
            if (stat1 + stat2 + stat3 + stat4) > 0:
                faultStr = "ALARM EVU Status nicht 0"
                faultState = 2
                # speicher in mqtt
            else:
                faultStr = ''
                faultState = 0
                
            if (bstat1 + bstat2 + bstat3) > 0:
                bfaultStr = "Battery ALARM Battery-Status nicht 0"
                bfaultState = 2
                # speicher in mqtt
            else:
                bfaultStr = ''
                bfaultState = 0    
            

            os.system('mosquitto_pub -r -t openWB/set/evu/faultState -m "' + str(faultState) + '"')
            os.system('mosquitto_pub -r -t openWB/set/evu/faultStr -m "' + str(faultStr) + '"')
            os.system('mosquitto_pub -r -t openWB/set/housebattery/faultState -m "' + str(bfaultState) + '"')
            os.system('mosquitto_pub -r -t openWB/set/housebattery/faultStr -m "' + str(bfaultStr) + '"')
            os.system('mosquitto_pub -r -t openWB/housebattery/soctarget -m "' + str(socsoll) + '"')                       

            # debug output of processing time and all response elements
            rct.dbglog(response.format_list(time.time() - start_time))
        except:
            print("-"*100)
            traceback.print_exc(file=sys.stdout)
            rct.close()

    rct = None

if __name__ == "__main__":
    main(sys.argv[1:])