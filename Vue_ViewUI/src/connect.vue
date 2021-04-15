<script type="text/javascript">
import axios from "axios";

const url = "http://127.0.0.1:8080/"

//管理员登录接口
export function login_a(username, password) {
  axios
      .post(url + "admin/login", {
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
export function createreport_a(timestamp) {
  axios
      .post(url + "admin/createreport", {
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
export function createwaterbills_a(date) {
  axios
      .post(url + "admin/createwaterbills", {
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
export function turnonoff_a(rid, action) {
  axios
      .post(url + "admin/turnonoff", {
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
export function settemp_a(rid, settemp) {
  axios
      .post(url + "admin/settemp", {

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
/*export function setpattern_a(rid, pattern)
{
    axios
    .post(url, {
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
export function setmode_a(rid, setmode) {
  axios
      .post(url + "admin/setmode", {
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
export function discount_a(rid, discount) {
  axios
      .post(url + "admin/discount", {
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
export function centerturnonoff_a(state) {
  axios
      .post(url + "admin/centerturnonoff", {
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
export function signin_r(phonenumber) {
  axios
      .post(url + "reception/signin", {
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
export function logout_r(rid) {
  axios
      .post(url + "reception/logout", {
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
/**
 * @deprecated 外部调用无法获取异步请求返回值
 * @param rid
 * @param password
 */
export function checkin_u_d(rid, password) {
  axios
      .post(url + "user/checkin", {
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

export function send_checkin_u(rid, password) {
  return (axios.post(url + "user/checkin", {
    rid: rid,
    password: password
  }));
}

export function checkin_u(rid, password) {
  send_checkin_u(rid, password)
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
export function turnonoff_u(rid, state) {
  axios
      .post(url + "user/turnonoff", {
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
export function settemp_u(rid, state) {
  axios
      .post(url + "user/settemp", {
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
export function setmode_u(rid, setmode) {
  axios
      .post(url + "user/setmode", {
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
export function showcast_u(rid) {
  axios
      .post(url + "user/showcost", {
        rid: rid,
        setmode: setmode
      })
      .then(response => {
        return {
          error_code: 0,
          data: {
            onoff: response.data.onoff,
            cost: response.data.cost
          }
        }
      })
      .catch(error => {
        console.log(error);
      });
}
</script>