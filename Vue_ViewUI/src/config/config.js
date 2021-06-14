import Env from './env';

let config = {
	env: Env,
	dev: {
		proxyTable: {
			'/api': {
				target: 'http://192.168.43.159:5000/',
				changeOrigin: true,
				pathRewrite: {
					'^/api': 'http://192.168.43.159:5000/'
				}
			}
		}
	}
};
export default config;