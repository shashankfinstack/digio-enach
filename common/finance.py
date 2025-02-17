from __future__ import annotations
from typing import Optional, List
from utils.misc import MiscUtils
from helpers.common.misc import IndianStates
from datetime import date

class FinancialDetail:
    def __init__(
        self,
        profit_loss: Optional[str] = None,
        year: Optional[str] = None,
        turn_over: Optional[str] = None,
    ) -> None:
        self.profit_loss = profit_loss 
        self.year = year 
        self.turn_over = turn_over 
    
    def to_dict(self) -> dict:
        return {
            "profit_loss": self.profit_loss,
            "year": self.year,
            "turn_over": self.turn_over,
        }

    @classmethod
    def from_dict(cls, d: dict) -> FinancialDetail:
        return cls(
            profit_loss=d.get('profitLoss'),
            year=d.get('year'),
            turn_over=d.get('turnOver'),
        )
    
class Transaction:
    def __init__(
        self,
        readerReadTime: Optional[str] = None,
        seqNo: Optional[str] = None,
        laneDirection: Optional[str] = None,
        tollPlazaGeocode: Optional[str] = None,
        tollPlazaName: Optional[str] = None,
        vehicleType: Optional[str] = None,
        vehicleRegNo: Optional[str] = None,
    ) -> None:
        self.readerReadTime = readerReadTime
        self.seqNo = seqNo
        self.laneDirection = laneDirection
        self.tollPlazaGeocode = tollPlazaGeocode
        self.tollPlazaName = tollPlazaName
        self.vehicleType = vehicleType
        self.vehicleRegNo = vehicleRegNo
    
    def to_dict(self) -> dict:
        return {
            "reader_read_time": self.readerReadTime,
            "seq_no": self.seqNo,
            "lane_direction": self.laneDirection,
            "toll_plaza_geocode": self.tollPlazaGeocode,
            "toll_plaza_name": self.tollPlazaName,
            "vehicle_type": self.vehicleType,
            "vehicle_reg_no": self.vehicleRegNo,
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> Transaction:
        return cls(
            readerReadTime=d.get('readerReadTime'),
            seqNo=d.get('seqNo'),
            laneDirection=d.get('laneDirection'),
            tollPlazaGeocode=d.get('tollPlazaGeocode'),
            tollPlazaName=d.get('tollPlazaName'),
            vehicleType=d.get('vehicleType'),
            vehicleRegNo=d.get('vehicleRegNo')
        )
    
class VehicleTxnList:
    def __init__(
        self,
        totalTagsInMsg: Optional[str] = None, 
        msgNum: Optional[str] = None, 
        totalTagsInresponse: Optional[str] = None, 
        totalMsg: Optional[str] = None, 
        txn: Optional[List[Transaction]] = None, 
    ) -> None:
        self.totalTagsInMsg = totalTagsInMsg
        self.msgNum = msgNum
        self.totalTagsInresponse = totalTagsInresponse
        self.totalMsg = totalMsg
        self.txn = txn
    
    def to_dict(self) -> dict:
        return {
            "total_tags_in_msg": MiscUtils.typecast_string(self.totalTagsInMsg,int,int),
            "msg_num": MiscUtils.typecast_string(self.msgNum,int,int),
            "total_tags_inresponse": MiscUtils.typecast_string(self.totalTagsInresponse,int,int),
            "total_msg": MiscUtils.typecast_string(self.totalMsg,int,int),
            "txn": self.txn,
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> Vehicle:
        if d is None:
            return None
        txnList = []
        for transaction in d.get('txn'):
            obj = Transaction.from_dict(transaction)
            txnList.append(obj.to_dict())
        return cls(
            totalTagsInMsg=d.get('totalTagsInMsg'),
            msgNum=d.get('msgNum'),
            totalTagsInresponse=d.get('totalTagsInresponse'),
            totalMsg=d.get('totalMsg'),
            txn=txnList
        )

class Vehicle:
    def __init__(
        self,
        errCode: Optional[str] = None,
        vehltxnList: Optional[VehicleTxnList] = None,
    ) -> None:
        self.errCode = errCode 
        self.vehltxnList = vehltxnList
    
    def to_dict(self) -> dict:
        return {
            "err_code": self.errCode,
            "vehltxn_list": self.vehltxnList,
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> Vehicle:
        return cls(
            errCode=d.get('errCode'),
            vehltxnList=VehicleTxnList.from_dict(d.get('vehltxnList')).to_dict() if VehicleTxnList.from_dict(d.get('vehltxnList')) is not None else None
        )

