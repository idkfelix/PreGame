import requests
import json
import os
import base64
import yaml

# Stop local unsecured warning
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

class Lockfile():
    # name,pid,port,password,protocol
    lockfile = open(os.getenv("LOCALAPPDATA")+"\Riot Games\Riot Client\Config\lockfile").read()
    slockfile = lockfile.split(":")
    name = slockfile[0]
    pid = slockfile[1]
    port = slockfile[2]
    passwd = slockfile[3]
    protocol = slockfile[4]

def GenPass64(passwd):
    rpasswd = f"riot:{passwd}"
    passBytes = rpasswd.encode("ascii")
    base64Bytes = base64.b64encode(passBytes)
    base64Pass = base64Bytes.decode('ascii')
    return base64Pass

def GetRegionShardString():
    with open(os.getenv("LOCALAPPDATA")+"\GreifSuite\config.yaml", "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
        RegionShardString = conf["region"]+"-1."+conf["shard"]
        return RegionShardString

class Get():

    def AccessToken(port, passwd64):
        url = f"https://127.0.0.1:{port}/entitlements/v1/token"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {passwd64}"
        }

        response = requests.request("GET", url, headers=headers, verify=False)
        loaded = json.loads(response.text)
        return loaded["accessToken"]

    def EToken(port, passwd64):
        url = f"https://127.0.0.1:{port}/entitlements/v1/token"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {passwd64}"
        }

        response = requests.request("GET", url, headers=headers, verify=False)
        loaded = json.loads(response.text)
        return loaded["token"]

    def PUUID(AccessToken):
        url = "https://auth.riotgames.com/userinfo"

        headers = {"Authorization": f"Bearer {AccessToken}"}
        
        response = requests.request("GET", url, headers=headers, verify=False)
        loaded = json.loads(response.text)

        return loaded["sub"]

    def MatchID():
        url = f"https://glz-{rsString}.a.pvp.net/core-game/v1/players/{puuid}"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        response = requests.request("GET", url, headers=headers, verify=False)
        loaded = json.loads(response.text)
        print(response.text)
        return loaded["MatchID"]
    
    def PreMatchID():
        url = f"https://glz-ap-1.ap.a.pvp.net/pregame/v1/players/{puuid}"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        response = requests.request("GET", url, headers=headers, verify=False)
        loaded = json.loads(response.text)
        return loaded["MatchID"]
    
    def PartyID():
        url = f"https://glz-{rsString}.a.pvp.net/parties/v1/players/{puuid}"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-ClientVersion": clientVersion,
            "X-Riot-Entitlements-JWT": eToken
        }

        response = requests.request("GET", url, headers=headers, verify=False)
        loaded = json.loads(response.text)
        return loaded["CurrentPartyID"]

    def AgentLUT():
        url = "https://valorant-api.com/v1/agents"

        response = requests.request("GET",url)
        loaded = json.loads(response.text)
        agents = {}
        for agent in loaded["data"]:
            agents[agent["displayName"]] = agent["uuid"]
        return agents
    
    def AgentIDs():
        url = "https://valorant-api.com/v1/agents"

        response = requests.request("GET",url)
        loaded = json.loads(response.text)
        agents = []
        for agent in loaded["data"]:
            agents.append(agent["uuid"])
        return agents

    def clientVersion():
        url = "https://valorant-api.com/v1/version"
        response = requests.request("GET",url)
        loaded = json.loads(response.text)
        version = str(loaded["data"]["riotClientVersion"])
        return version.replace('shipping-','')
        
class Chat():

    def Message(cid, msg):
        url = f"https://127.0.0.1:{rport}/chat/v6/messages/"

        payload = {
            "cid": cid,
            "message": msg,
            "type": "groupchat"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {passwd}"
        }

        requests.request("POST", url, json=payload, headers=headers, verify=False)

    def getPartyCid():
        url = f"https://127.0.0.1:{rport}/chat/v6/conversations/ares-parties"

        headers = {"Authorization": f"Basic {passwd}"}

        response = requests.request("GET", url, headers=headers, verify=False)

        loaded = json.loads(response.text)
        return loaded["conversations"][0]["cid"]

    def getGameCid():
        url = f"https://127.0.0.1:{rport}/chat/v6/conversations/ares-coregame"

        headers = {"Authorization": f"Basic {passwd}"}

        response = requests.request("GET", url, headers=headers, verify=False)

        loaded = json.loads(response.text)
        return loaded["conversations"][0]["cid"]
    
    def getTeamCid():
        url = f"https://127.0.0.1:{rport}/chat/v6/conversations/ares-coregame"

        headers = {"Authorization": f"Basic {passwd}"}

        response = requests.request("GET", url, headers=headers, verify=False)

        loaded = json.loads(response.text)
        return loaded["conversations"][1]["cid"]

class Match():
        
    def Dissociate(matchID):
        url = f"https://glz-ap-1.ap.a.pvp.net/core-game/v1/players/{puuid}/disassociate/{matchID}"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        requests.request("POST", url, headers=headers, verify=False)

    def Dodge(preMatchID):
        url = f"https://glz-{rsString}.a.pvp.net/pregame/v1/matches/{preMatchID}/quit"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        requests.request("POST", url, headers=headers, verify=False)

    def AgentSelect(preMatchID, agentID):
        url = f"https://glz-{rsString}.a.pvp.net/pregame/v1/matches/{preMatchID}/select/{agentID}"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        requests.request("POST", url, headers=headers, verify=False)

    def AgentLock(preMatchID, agentID):
        url = f"https://glz-{rsString}.a.pvp.net/pregame/v1/matches/{preMatchID}/lock/{agentID}"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        requests.request("POST", url, headers=headers, verify=False)

class Party():

    def StartCustom():
        partyID = Get.PartyID()
        url = f"https://glz-{rsString}.a.pvp.net/parties/v1/parties/{partyID}/startcustomgame"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-ClientVersion": clientVersion,
            "X-Riot-Entitlements-JWT": eToken
        }

        requests.request("POST", url, headers=headers, verify=False)

    def LeaveMatchmaking():
        partyID = Get.PartyID()
        url = f"https://glz-{rsString}.a.pvp.net/parties/v1/parties/{partyID}/matchmaking/leave"

        headers = {
            "Authorization": f"Bearer {accessToken}",
            "X-Riot-Entitlements-JWT": eToken
        }

        requests.request("POST", url, headers=headers, verify=False)

rport = Lockfile.port
passwd = GenPass64(Lockfile.passwd)

rsString = GetRegionShardString()

accessToken = Get.AccessToken(rport, passwd)
eToken = Get.EToken(rport, passwd)
puuid = Get.PUUID(accessToken)

clientVersion = Get.clientVersion()