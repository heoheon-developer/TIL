import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		main: {
			customerList: [],
			selectedRows: [],
			type: '',
			memberList: [],
			customer_selectBox_list: [],
			customer_detail_info: null,
			member_detail_info: null,
			global_company_id: null,
			systemManagerList: [],
			payload: null,
			noticeList: [],
			qnaList: []
		},
		loading: false,
		toastType: 0,
		toastMsg: ''
	},
	mutations: {
		getLists(state, payload) {
			state.main.type = payload['type'];
			let listing = payload['data']['data'];
			if (payload['type'] === 'customer') {
				for (let row of listing) {
					state.main.customerList.push(row);
				}
			} else if (payload['type'] === 'member') {
				for (let row of listing) {
					state.main.memberList.push(row);
				}
			} else if (payload['type'] === 'system-manager') {
				for (let row of listing) {
					state.main.systemManagerList.push(row);
				}
			} else if (payload['type'] === 'notice') {
				for (let row of listing) {
					state.main.noticeList.push(row);
				}
			} else if (payload['type'] === 'qna') {
				for (let row of listing) {
					state.main.qnaList.push(row);
				}
			}

		},
		// 구성원 관리의 고객사 리스트를 설정
		setCustomerList(state, payload) {
			let listing = payload['data']['data'];
			state.main.type = payload['type'];
			for (let row of listing) {
				state.main.customer_selectBox_list.push(row);
			}
		},
		init(state, payload) {
			// 상태값 초기화
			if (payload['type'] === 'customer') {
				state.main.customerList = [];
				state.main.global_company_id = null;
			} else if (payload['type'] === 'member') {
				state.main.memberList = [];
				state.main.selectedRows = [];
			} else if (payload['type'] === 'member-select') {
				state.main.customer_selectBox_list = [];
			} else if (payload['type'] === 'system-manager') {
				state.main.systemManagerList = [];
			} else if (payload['type'] === 'notice') {
				state.main.noticeList = [];
			}else if (payload['type'] === 'qna') {
				state.main.qnaList = [];
			}
		},
		start: (state) => state.loading = true,
		end: (state) => state.loading = false,
		toastMsg(state, payload) {
			state.toastType = payload.toastType
			state.toastMsg = payload.toastMsg
			setTimeout(() => {
				state.toastType = 0
				state.toastMsg = ''
			}, 3000)
		},

	},
	actions: {
		getCustomerInfo: async function ({commit}, payload) {
			// 고객사 관리 - 리스트 취득
			let customer_info = payload['formData']
			let responseCustomer = await this._vm.axios.post('/admin/customers/', customer_info)
			let data = responseCustomer.data
			console.log("data", data)
			if (payload['type'] === 'customer') {
				commit('init', {type: 'customer'});
				commit('getLists', {type: 'customer', data})
				// 구성원 관리 - 고객사 selectbox 표시용
			} else if (payload['type'] === 'member') {
				commit('setCustomerList', {type: 'member', data})
			}
		},
		getMemberInfo: async function ({commit}, payload) {
			// 구성원 관리 - 리스트 취득
			let member_info = payload['formData']
			let responseMember = await this._vm.axios.post('/admin/members/', member_info)
			let data = responseMember.data
			commit('init', {type: 'member'});
			commit('getLists', {type: 'member', data})
		},
		getSystemManagerInfo: async function ({commit}, payload) {
			// 시스템관리자 - 리스트 취득
			let system_manager_info = payload['formData']
			let responseSystemManager = await this._vm.axios.post('/admin/system-managers/', system_manager_info)
			let data = responseSystemManager.data
			commit('init', {type: 'system-manager'});
			commit('getLists', {type: 'system-manager', data})
		},

		getNoticeInfo: async function ({commit}, payload) {
			// 공지사항 - 리스트 취득
			let notice_info = payload['formData']
			let responseNotice = await this._vm.axios.post('/admin/notices/', notice_info)
			let data = responseNotice.data
			commit('init', {type: 'notice'});
			commit('getLists', {type: 'notice', data})
		},
		getQnaInfo: async function ({commit}, payload) {
			// 공지사항 - 리스트 취득
			let qna_info = payload['formData']
			let responseNotice = await this._vm.axios.post('/admin/qna-list/', qna_info)
			let data = responseNotice.data
			console.log("QNA", data)
			commit('init', {type: 'qna'});
			commit('getLists', {type: 'qna', data})
		}

	},
	modules: {},

})
