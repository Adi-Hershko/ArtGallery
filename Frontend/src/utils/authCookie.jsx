import Cookies from 'js-cookie';

export const headers = {
    'Cookie': 'token=' + Cookies.get("token")
}

export const set = (value) => {
    Cookies.set("token", value)
};
