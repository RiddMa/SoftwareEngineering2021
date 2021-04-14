




<!--deprecated!!!!!-->





<script type="text/javascript">
import axios from "axios";
import VueAxios from 'vue-axios'

export function foo(){
  console.log("hello");
}
//管理员登录接口
export function login(username, password)
{
    axios
    .post("http://xx.com/admin/login", {
        no: 1,
        username: username,
        password: password
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
                uid: response.data.uid,
                username: response.data.username,
                token: "XXX"
            }
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员生成报表接口
export function createreport(timestamp)
{
    axios
    .post("http://xx.com/admin/createreport", {
        no: 2,
        timestamp: timestamp
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
                rid: response.data.rid,
                state: response.data.state,
                temp: response.data.temp,
                mode: response.data.mode,
                discount: response.data.discount
            }
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员查看流水接口
export function createwaterbills(date)
{
    axios
    .post("http://xx.com/admin/createwaterbills", {
        no: 3,
        date: date
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
                rid: response.data.rid,
                time: response.data.time,
                account: response.data.account
            }
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员控制房间空调开启与关闭
export function admin_turnonoff(rid, action)
{
    axios
    .post("http://xx.com/admin/turnonoff", {
        no: 4,
        rid: rid,
        action: action
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员控制房间空调温度
export function settemp(rid, settemp)
{
    axios
    .post("http://xx.com/admin/settemp", {
        no: 5,
        rid: rid,
        settemp: settemp
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员控制制冷制热
/*export function setpattern(rid, pattern)
{
    axios
    .post("url", {
        no: 6,
        rid: rid,
        pattern: pattern
    })
    .then(response => {
        return {
            error_code: 0,
        }
    })
    .catch(error => {
        console.log(error);
    });
}*/

//管理员控制房间风速挡位
export function admin_setmode(rid, setmode)
{
    axios
    .post("http://xx.com/admin/setmode", {
        no: 6,
        rid: rid,
        setmode: setmode
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员控制单个房间的优惠力度
export function discount(rid, discount)
{
    axios
    .post("http://xx.com/admin/discount", {
        no: 7,
        rid: rid,
        discount: discount
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//管理员开关所有空调
export function centerturnonoff(state)
{
    axios
    .post("http://xx.com/admin/centerturnonoff", {
        no: 8,
        state: state
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//前台办理入住
export function signin(phonenumber)
{
    axios
    .post("http://xx.com/reception/signin", {
        no: 9,
        phonenumber: phonenumber
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
              name: response.data.name,
              rid: response.data.rid,
              password: response.data.password
            }
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//前台办理退房
export function logout(rid)
{
    axios
    .post("http://xx.com/reception/logout", {
        no: 10,
        rid: rid
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
                duration: response.data.duration,
                price: response.data.price
            }
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//用户刷卡进入房间
export function client_login(rid, password)
{
    axios
    .post("http://xx.com/user/checkin", {
        no: 11,
        rid: rid,
        password: password
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
                uid: response.data.uid,
                username: response.data.username,
                token: response.data.token
            }
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//用户控制空调开关
export function client_turnonoff(rid, state)
{
    axios
    .post("http://xx.com/user/turnonoff", {
        no: 12,
        rid: rid,
        state: state
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//用户控制房间空调温度
export function client_settemp(rid, state)
{
    axios
    .post("http://xx.com/user/settemp", {
        no: 13,
        rid: rid,
        state: state
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//用户控制房间空调风速
export function setmode(rid, setmode)
{
    axios
    .post("http://xx.com/user/setmode", {
        no: 14,
        rid: rid,
        setmode: setmode
    })
    .then(response => {
        return {
            error_code: 0
        }
    })
    .catch(error => {
        console.log(error);
    });
}

//用户界面更新显示金额
export function showcast(rid)
{
    axios
    .post("http://xx.com/user/showcost", {
        no: 15,
        rid: rid,
        setmode: setmode
    })
    .then(response => {
        return {
            error_code: 0,
            data: {
                onoff:  response.data.onoff,
                cost:  response.data.cost
              }
        }
    })
    .catch(error => {
        console.log(error);
    });
}
</script>