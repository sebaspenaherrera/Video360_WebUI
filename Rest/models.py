'''
Summary: This class establishes the PYDANTIC models for data validation and serialization
Author: Sebastian Peñaherrera
Date: 07/10/2023
Status: Under development
'''

from pydantic import BaseModel, Field
from typing import Dict
from typing import List


# Class SampleStats for the model contained in each value inside the dict
class KQI(BaseModel):
    timestamp: float
    initTime: float
    stallTime: float
    overallStallTime: float
    bufferTime: float
    rtt_ping: float
    rtt: float
    estimatedBWExoplayer: float
    tx_rate: float
    rx_rate: float
    tx_packetRate: int
    rx_packetRate: int
    width: int
    height: int
    resolution: str
    res_switches: int
    res_profile: int
    displayed_frameRate: float
    encoded_frameRate: float
    screen_frameRate: float
    min_screen_frameRate: float
    max_screen_frameRate: float
    duplicatedFrames: int
    perfectFrames: float
    skippedFrames: int
    unityDroppedFrames: int
    playerDescription: str
    maxFrameNumber: int
    durationFrames: int
    durationMedia: float
    hasAudio: bool
    hasVideo: bool
    isStalled: bool
    isPlaying: bool
    isBuffering: bool


class Signal(BaseModel):
    pci: str | None = None
    sc: str | None = None
    cell_id: str | None = None
    rsrq: str | None = None
    rsrp: str | None = None
    rssi: str | None = None
    sinr: str | None = None
    rscp: str | None = None
    ecio: str | None = None
    mode: str | None = None
    ulbandwidth: str | None = None
    dlbandwidth: str | None = None
    txpower_PPusch: str | None = None
    txpower_PPucch: str | None = None
    txpower_PSrs: str | None = None
    txpower_PPrach: str | None = None
    tdd: str | None = None
    ul_mcs: str | None = None
    dl_mcs_mcsDownCarrier1Code0: int | None = None
    dl_mcs_mcsDownCarrier1Code1: int | None = None
    earfcn_DL: int | None = None
    earfcn_UL: int | None = None
    rrc_status: int | None = None
    rac: str | None = None
    lac: str | None = None
    tac: str | None = None
    band: str | None = None
    nei_cellid: str | None = None
    plmn: str | None = None
    ims: str | None = None
    wdlfreq: str | None = None
    lteulfreq: str | None = None
    ltedlfreq: str | None = None
    transmode: str | None = None
    enodeb_id: str | None = None
    cqi0: int | None = None
    cqi1: int | None = None
    ulfrequency: str | None = None
    dlfrequency: str | None = None
    nrulbandwidth: str | None = None
    nrdlbandwidth: str | None = None
    nrulmcs: str | None = None
    nrdlmcs_NRmcsDownCarrier1Code0: int | None = None
    nrdlmcs_NRmcsDownCarrier1Code1: int | None = None
    nrtxpower_PPusch: str | None = None
    nrtxpower_PPucch: str | None = None
    nrtxpower_PSrs: str | None = None
    nrtxpower_PPrach: str | None = None
    nrearfcn_DL: int | None = None
    nrearfcn_UL: int | None = None
    nrulfreq: str | None = None
    nrdlfreq: str | None = None
    nrsinr: str | None = None
    nrrsrp: str | None = None
    nrrsrq: str | None = None
    nrbler: str | None = None
    nrrank: str | None = None
    nrcqi0: int | None = None
    nrcqi1: int | None = None
    scc_pci: str | None = None
    arfcn: str | None = None
    bsic: str | None = None
    rxlev: str | None = None


class Traffic(BaseModel):
    CurrentConnectTime: int | None = None
    CurrentUpload: int | None = None
    CurrentDownload: int | None = None
    CurrentDownloadRate: int | None = None
    CurrentUploadRate: int | None = None
    TotalUpload: int | None = None
    TotalDownload: int | None = None
    TotalConnectTime: int | None = None
    showtraffic: int | None = None


class Info(BaseModel):
    DeviceName: str | None = None
    SerialNumber: str | None = None
    Imei: str | None = None
    Imsi: str | None = None
    Iccid: str | None = None
    Msisdn: str | None = None
    HardwareVersion: str | None = None
    SoftwareVersion: str | None = None
    WebUIVersion: str | None = None
    MacAddress1: str | None = None
    MacAddress2: str | None = None
    WanIPAddress: str | None = None
    wan_dns_address: str | None = None
    WanIPv6Address: str | None = None
    wan_ipv6_dns_address: str | None = None
    ProductFamily: str | None = None
    Classify: str | None = None
    supportmode: str | None = None
    workmode: str | None = None
    submask: str | None = None
    Mccmnc: str | None = None
    iniversion: str | None = None
    uptime: int | None = None
    ImeiSvn: str | None = None
    WifiMacAddrWl0: str | None = None
    WifiMacAddrWl1: str | None = None
    spreadname_en: str | None = None
    spreadname_zh: str | None = None


class CrowdCellSample(BaseModel):
    timestamp: float | None = None
    cell_id: float | None = None
    dl_bitrate: float | None = None
    ul_bitrate: float | None = None
    dl_tx: float | None = None
    ul_tx: float | None = None
    dl_err: float | None = None
    ul_err: float | None = None
    dl_retx: float | None = None
    ul_retx: float | None = None
    dl_use_min: float | None = None
    dl_use_max: float | None = None
    dl_use_avg: float | None = None
    ul_use_min: float | None = None
    ul_use_max: float | None = None
    ul_use_avg: float | None = None
    dl_sched_users_min: float | None = None
    dl_sched_users_max: float | None = None
    dl_sched_users_avg: float | None = None
    ul_sched_users_min: float | None = None
    ul_sched_users_max: float | None = None
    ul_sched_users_avg: float | None = None
    ue_count_min: float | None = None
    ue_count_max: float | None = None
    ue_count_avg: float | None = None
    ue_active_count_min: float | None = None
    ue_active_count_max: float | None = None
    ue_active_count_avg: float | None = None
    ue_inactive_count_min: float | None = None
    ue_inactive_count_max: float | None = None
    ue_inactive_count_avg: float | None = None
    drb_count_min: float | None = None
    drb_count_max: float | None = None
    drb_count_avg: float | None = None
    dl_gbr_use_min: float | None = None
    dl_gbr_use_max: float | None = None
    dl_gbr_use_avg: float | None = None
    ul_gbr_use_min: float | None = None
    ul_gbr_use_max: float | None = None
    ul_gbr_use_avg: float | None = None


class CrowdcellStats(BaseModel):
    Crowdcell_stats: List[CrowdCellSample]


class ProcessInfo(BaseModel):
    timestamp: float | None = None
    type: str | None = None
    pid: int | None = None
    name: str | None = None
    cpu_percentage : float | None = Field(None, alias='cpu%')
    core: int | None = None


class CPUMonitoring(BaseModel):
    CPU_stats : List[ProcessInfo]


class CPEStats(BaseModel):
    signal: Signal | None = None
    traffic: Traffic | None = None
    info: Info | None = None


class SampleStats(BaseModel):
    Service: KQI
    CPE: CPEStats | None = None


class SessionStats(BaseModel):
    data: dict[int, SampleStats]


class Config:
    allow_population_by_field_name = True

# Example of a body for a POST operation
example_POST_testbed = {
    "data":{
        "0":{
            "Service":{
                "timestamp":"1700065517954",
                "initTime":0.32171450000896587,
                "stallTime":0.6599999852478504,
                "overallStallTime":0.6599999852478504,
                "bufferTime":101.125,
                "rtt_ping":16.0,
                "rtt":310.93,
                "estimatedBWExoplayer":0.0,
                "tx_rate":0.0,
                "rx_rate":0.0,
                "tx_packetRate":0,
                "rx_packetRate":0,
                "width":1280,
                "height":720,
                "resolution":"1280x720",
                "res_switches":0,
                "res_profile":0,
                "displayed_frameRate":1.9913451671600342,
                "encoded_frameRate":24.0,
                "screen_frameRate":307.8643497356057,
                "min_screen_frameRate":110.6515940958436,
                "max_screen_frameRate":380.674535241158,
                "duplicatedFrames":0,
                "perfectFrames":0.0,
                "skippedFrames":0,
                "unityDroppedFrames":0,
                "playerDescription":"",
                "maxFrameNumber":14314,
                "durationFrames":14315,
                "durationMedia":596.4733333333334,
                "hasAudio":True,
                "hasVideo":True,
                "isStalled":True,
                "isPlaying":True,
                "isBuffering":False
            },
            "CPE":{
                "signal":{
                    "pci":"1",
                    "sc":"",
                    "cell_id":"27447297",
                    "rsrq":"-4.0dB",
                    "rsrp":"-63dBm",
                    "rssi":"-37dBm",
                    "sinr":"27dB",
                    "rscp":"",
                    "ecio":"",
                    "mode":"7",
                    "ulbandwidth":"20MHz",
                    "dlbandwidth":"20MHz",
                    "txpower_PPusch":"-4dBm",
                    "txpower_PPucch":"-5dBm",
                    "txpower_PSrs":"-5dBm",
                    "txpower_PPrach":"-5dBm",
                    "tdd":"",
                    "ul_mcs":"mcsUpCarrier1:21",
                    "dl_mcs_mcsDownCarrier1Code0":"26",
                    "dl_mcs_mcsDownCarrier1Code1":"26",
                    "earfcn_DL":"300",
                    "earfcn_UL":"18300",
                    "rrc_status":"1",
                    "rac":"",
                    "lac":"",
                    "tac":"1",
                    "band":"1",
                    "nei_cellid":"",
                    "plmn":"00101",
                    "ims":"0",
                    "wdlfreq":"",
                    "lteulfreq":"19500",
                    "ltedlfreq":"21400",
                    "transmode":"TM[3]",
                    "enodeb_id":"0107216",
                    "cqi0":"13",
                    "cqi1":"2",
                    "ulfrequency":"1950000kHz",
                    "dlfrequency":"2140000kHz",
                    "nrulbandwidth":"40MHz",
                    "nrdlbandwidth":"40MHz",
                    "nrulmcs":"NRmcsUpCarrier1:4",
                    "nrdlmcs_NRmcsDownCarrier1Code0":"23",
                    "nrdlmcs_NRmcsDownCarrier1Code1":"0",
                    "nrtxpower_PPusch":"-29dBm",
                    "nrtxpower_PPucch":"-39dBm",
                    "nrtxpower_PSrs":"-34dBm",
                    "nrtxpower_PPrach":"-41dBm",
                    "nrearfcn_DL":"632626",
                    "nrearfcn_UL":"632626",
                    "nrulfreq":"3489400kHz",
                    "nrdlfreq":"3489400kHz",
                    "nrsinr":"27dB",
                    "nrrsrp":"-74dBm",
                    "nrrsrq":"-10.0dB",
                    "nrbler":"",
                    "nrrank":"",
                    "nrcqi0":"32639",
                    "nrcqi1":"32639",
                    "scc_pci":"",
                    "arfcn":"",
                    "bsic":"",
                    "rxlev":""
                },
                "traffic":{
                    "CurrentConnectTime":"953",
                    "CurrentUpload":"5251805",
                    "CurrentDownload":"18224475",
                    "CurrentDownloadRate":"130",
                    "CurrentUploadRate":"0",
                    "TotalUpload":"5251805",
                    "TotalDownload":"18224475",
                    "TotalConnectTime":"953",
                    "showtraffic":"1"
                },
                "info":{
                    "DeviceName":"H122-373",
                    "SerialNumber":"49VUT21205001341",
                    "Imei":"866887043517450",
                    "Imsi":"001010123456789",
                    "Iccid":"8988211910000023054",
                    "Msisdn":"",
                    "HardwareVersion":"WL1H122M",
                    "SoftwareVersion":"11.0.2.20(H329SP2C182)",
                    "WebUIVersion":"WEBUI 11.0.2.1(W2SP9C182)",
                    "MacAddress1":"F0:55:01:EB:86:31",
                    "MacAddress2":"",
                    "WanIPAddress":"192.168.2.2",
                    "wan_dns_address":"8.8.8.8",
                    "WanIPv6Address":"",
                    "wan_ipv6_dns_address":"",
                    "ProductFamily":"LTE",
                    "Classify":"cpe",
                    "supportmode":"LTE|WCDMA|GSM",
                    "workmode":"LTE",
                    "submask":"255.255.255.255",
                    "Mccmnc":"00101",
                    "iniversion":"H122-373-CUST 10.0.3.1(C182)",
                    "uptime":"436973",
                    "ImeiSvn":"01",
                    "WifiMacAddrWl0":"F0:55:01:EB:86:32",
                    "WifiMacAddrWl1":"F0:55:01:EB:86:36",
                    "spreadname_en":"HUAWEI 5G CPE Pro 2",
                    "spreadname_zh":"华为 5G CPE Pro 2"
                }
            }
        }
    }
}

example_POST_demo = {
    "Service":{
        "timestamp":"1700067537761",
        "initTime":0.19348245799483267,
        "stallTime":0.0,
        "overallStallTime":0.6199999861419201,
        "bufferTime":120.04166666666667,
        "rtt_ping":25.0,
        "rtt":155.2,
        "estimatedBWExoplayer":0.0,
        "tx_rate":0.0,
        "rx_rate":0.0,
        "tx_packetRate":0,
        "rx_packetRate":0,
        "width":1280,
        "height":720,
        "resolution":"1280x720",
        "res_switches":0,
        "res_profile":0,
        "displayed_frameRate":23.904218673706056,
        "encoded_frameRate":24.0,
        "screen_frameRate":350.65440014242497,
        "min_screen_frameRate":81.72049331165469,
        "max_screen_frameRate":527.4726029626378,
        "duplicatedFrames":0,
        "perfectFrames":0.0,
        "skippedFrames":0,
        "unityDroppedFrames":0,
        "playerDescription":"",
        "maxFrameNumber":14314,
        "durationFrames":14315,
        "durationMedia":596.4733333333334,
        "hasAudio":True,
        "hasVideo":True,
        "isStalled":False,
        "isPlaying":True,
        "isBuffering":False
    },
    "CPE":{
        "signal":{
            "pci":"1",
            "sc":"",
            "cell_id":"27447297",
            "rsrq":"-4.0dB",
            "rsrp":"-63dBm",
            "rssi":"-37dBm",
            "sinr":"27dB",
            "rscp":"",
            "ecio":"",
            "mode":"7",
            "ulbandwidth":"20MHz",
            "dlbandwidth":"20MHz",
            "txpower_PPusch":"-4dBm",
            "txpower_PPucch":"-5dBm",
            "txpower_PSrs":"-4dBm",
            "txpower_PPrach":"-5dBm",
            "tdd":"",
            "ul_mcs":"mcsUpCarrier1:23",
            "dl_mcs_mcsDownCarrier1Code0":"26",
            "dl_mcs_mcsDownCarrier1Code1":"26",
            "earfcn_DL":"300",
            "earfcn_UL":"18300",
            "rrc_status":"1",
            "rac":"",
            "lac":"",
            "tac":"1",
            "band":"1",
            "nei_cellid":"",
            "plmn":"00101",
            "ims":"0",
            "wdlfreq":"",
            "lteulfreq":"19500",
            "ltedlfreq":"21400",
            "transmode":"TM[3]",
            "enodeb_id":"0107216",
            "cqi0":"14",
            "cqi1":"2",
            "ulfrequency":"1950000kHz",
            "dlfrequency":"2140000kHz",
            "nrulbandwidth":"40MHz",
            "nrdlbandwidth":"40MHz",
            "nrulmcs":"NRmcsUpCarrier1:6",
            "nrdlmcs_NRmcsDownCarrier1Code0":"23",
            "nrdlmcs_NRmcsDownCarrier1Code1":"0",
            "nrtxpower_PPusch":"-31dBm",
            "nrtxpower_PPucch":"-39dBm",
            "nrtxpower_PSrs":"-34dBm",
            "nrtxpower_PPrach":"-41dBm",
            "nrearfcn_DL":"632626",
            "nrearfcn_UL":"632626",
            "nrulfreq":"3489400kHz",
            "nrdlfreq":"3489400kHz",
            "nrsinr":"27dB",
            "nrrsrp":"-74dBm",
            "nrrsrq":"-10.0dB",
            "nrbler":"",
            "nrrank":"",
            "nrcqi0":"32639",
            "nrcqi1":"32639",
            "scc_pci":"",
            "arfcn":"",
            "bsic":"",
            "rxlev":""
        },
        "traffic":{
            "CurrentConnectTime":"0",
            "CurrentUpload":"0",
            "CurrentDownload":"0",
            "CurrentDownloadRate":"0",
            "CurrentUploadRate":"0",
            "TotalUpload":"0",
            "TotalDownload":"0",
            "TotalConnectTime":"0",
            "showtraffic":"1"
        },
        "info":{
            "DeviceName":"H122-373",
            "SerialNumber":"49VUT21205001341",
            "Imei":"866887043517450",
            "Imsi":"001010123456789",
            "Iccid":"8988211910000023054",
            "Msisdn":"",
            "HardwareVersion":"WL1H122M",
            "SoftwareVersion":"11.0.2.20(H329SP2C182)",
            "WebUIVersion":"WEBUI 11.0.2.1(W2SP9C182)",
            "MacAddress1":"F0:55:01:EB:86:31",
            "MacAddress2":"",
            "WanIPAddress":"192.168.2.2",
            "wan_dns_address":"8.8.8.8",
            "WanIPv6Address":"",
            "wan_ipv6_dns_address":"",
            "ProductFamily":"LTE",
            "Classify":"cpe",
            "supportmode":"LTE|WCDMA|GSM",
            "workmode":"LTE",
            "submask":"255.255.255.255",
            "Mccmnc":"00101",
            "iniversion":"H122-373-CUST 10.0.3.1(C182)",
            "uptime":"438993",
            "ImeiSvn":"01",
            "WifiMacAddrWl0":"F0:55:01:EB:86:32",
            "WifiMacAddrWl1":"F0:55:01:EB:86:36",
            "spreadname_en":"HUAWEI 5G CPE Pro 2",
            "spreadname_zh":"华为 5G CPE Pro 2"
        }
    }
}


example_GET_crowdcell_stats = {
    "timestamp": 1718803968.640493,
    "cell_id": 1,
    "dl_bitrate": 477780,
    "ul_bitrate": 320,
    "dl_tx": 2,
    "ul_tx": 2,
    "dl_err": 0,
    "ul_err": 4,
    "dl_retx": 0,
    "ul_retx": 36,
    "dl_use_min": 0,
    "dl_use_max": 0.264,
    "dl_use_avg": 0.009,
    "ul_use_min": 0.038,
    "ul_use_max": 0.16,
    "ul_use_avg": 0.068,
    "dl_sched_users_min": 0,
    "dl_sched_users_max": 1,
    "dl_sched_users_avg": 0.002,
    "ul_sched_users_min": 0,
    "ul_sched_users_max": 1,
    "ul_sched_users_avg": 0.25,
    "ue_count_min": 4,
    "ue_count_max": 5,
    "ue_count_avg": 4.872,
    "ue_active_count_min": 4,
    "ue_active_count_max": 5,
    "ue_active_count_avg": 4.859,
    "ue_inactive_count_min": 0,
    "ue_inactive_count_max": 0,
    "ue_inactive_count_avg": 0,
    "drb_count_min": 1,
    "drb_count_max": 1,
    "drb_count_avg": 1.0,
    "dl_gbr_use_min": 0,
    "dl_gbr_use_max": 0,
    "dl_gbr_use_avg": 0,
    "ul_gbr_use_min": 0,
    "ul_gbr_use_max": 0,
    "ul_gbr_use_avg": 0
},
{
    "timestamp": 1718803969.640602,
    "cell_id": 1,
    "dl_bitrate": 8740,
    "ul_bitrate": 420,
    "dl_tx": 1,
    "ul_tx": 3,
    "dl_err": 1,
    "ul_err": 24,
    "dl_retx": 6,
    "ul_retx": 123,
    "dl_use_min": 0,
    "dl_use_max": 1.0,
    "dl_use_avg": 0.019,
    "ul_use_min": 0.038,
    "ul_use_max": 0.16,
    "ul_use_avg": 0.073,
    "dl_sched_users_min": 0,
    "dl_sched_users_max": 1,
    "dl_sched_users_avg": 0.011,
    "ul_sched_users_min": 0,
    "ul_sched_users_max": 1,
    "ul_sched_users_avg": 0.781,
    "ue_count_min": 4,
    "ue_count_max": 4,
    "ue_count_avg": 4.0,
    "ue_active_count_min": 4,
    "ue_active_count_max": 4,
    "ue_active_count_avg": 4.0,
    "ue_inactive_count_min": 0,
    "ue_inactive_count_max": 0,
    "ue_inactive_count_avg": 0,
    "drb_count_min": 1,
    "drb_count_max": 1,
    "drb_count_avg": 1.0,
    "dl_gbr_use_min": 0,
    "dl_gbr_use_max": 0,
    "dl_gbr_use_avg": 0,
    "ul_gbr_use_min": 0,
    "ul_gbr_use_max": 0,
    "ul_gbr_use_avg": 0
}