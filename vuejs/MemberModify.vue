<template>
	<!-- 구성원 수정 팝업 -->
	<div class="layer_popup" v-if="visible_modify">
		<div class="inner">
			<h3>구성원 수정</h3>
			<div class="detail_cont">
				<fieldset class="share_form">
					<legend>구성원 수정 설정</legend>
					<div>
						<span class="category"><label for="">이메일</label></span>
						<span class="field"><input type="text" id="" readonly v-model="email"/></span>
					</div>
					<div>
						<span class="category"><label for="">이름 <b>*</b></label></span>
						<span class="field"><input type="text" id="" v-model="name"/></span>
					</div>
					<div>
						<span class="category"><label for="">부서</label></span>
						<span class="field"><input type="text" id="" v-model="department"/></span>
					</div>
					<div>
						<span class="category"><label for="">권한</label></span>
						<span class="field">
						<span class="basic_select selectbox_ui" >
							<b class="selected_txt">사용자</b>
							<select title="상태 설정" v-model="authority" @change="changeValue">
								<option value="USER"  v-bind:selected="authority === 'USER'">사용자</option>
								<option value="MANAGER"  v-bind:selected="authority === 'MANAGER'">매니저</option>
								<option value="ADMIN"  v-bind:selected="authority === 'ADMIN'">관리자</option>
							</select>
						</span>
					</span>
					</div>
					<div>
						<span class="category"><label for="">용량</label></span>
						<span class="field"><input type="text" id="" v-model="data_limit"/> GB</span>
					</div>
					<div>
						<span class="category"><label for="">만료일</label></span>
						<span class="field">
						<span class="basic_datepicker">
							<datepicker v-model="expiration_date" :format="customFormatter"></datepicker>
							<button type="button"><img src="../../../assets/images/component/btn_calendar.png" alt="날짜선택"></button>
							<button type="button" class="del"><img src="../../../assets/images/component/btn_input_del.png" alt="날짜삭제"></button>
						</span>
					</span>
					</div>
					<p><label for=""><input type="checkbox" title="선택">콜드 드라이브 사용</label></p>
				</fieldset>
			</div>

			<div class="btn_set">
				<div class="right">
					<button type="button" class="btn_basic cancel" @click="handleWrapperClick">취소
					</button>
					<!--					<button type="button" class="btn_basic submit" :disabled="disabled">완료</button>-->
					<button type="button" class="btn_basic submit" @click="save">완료
					</button>
				</div>
			</div>
			<button class="btn_close" @click="handleWrapperClick"><img
				src="../../../assets/images/component/btn_popup_close.png" alt="닫기"/></button>
		</div>

	</div>

</template>

<script>
    import moment from 'moment/moment'
	import Datepicker from 'vuejs-datepicker'


	export default {

		components:{

			Datepicker

		},
		props: {
			visible_modify: {
				type: Boolean,
				require: true,
				default: false
			},
			detail: {
				type: Object,
				require: true,
				default: false
			}
		},
		computed: {},
		data() {
			return {
				email: '',
				name: '',
				department: '',
				authority: '',
				expiration_date: '',
				data_limit: null,
				use_cold_drive: null,
				btn_disabled: true,
			}
		},
		methods: {
			async getMemberDetailInfo() {
				let formData = new FormData();
				formData.append('id', this.detail.id);
				let responseData = await this.axios.post('/admin/member/', formData)
				this.email = responseData['data']['data']['email']
				this.name = responseData['data']['data']['name']
				this.department = responseData['data']['data']['department']
				this.authority = responseData['data']['data']['authority']
				this.data_limit = responseData['data']['data']['data_limit']
				this.expiration_date = this.customFormatter(responseData['data']['data']['expiration_date'])
			},
			customFormatter(date){
				return moment(date).format('YYYY-MM-DD');
			},
			handleWrapperClick() {
				this.$emit('update:visible_modify', false)
				$(".modal_bg").hide()
			},
			changeValue(){

				console.log("this.aut", this.authority)

			},
			save() {


				console.log("this.authority", this.authority)
				let formData = new FormData();
				formData.append('id', this.detail.id);
				formData.append('name', this.name);
				formData.append('department', this.department);
				formData.append('authority', this.authority);
				formData.append('expiration_date', this.expiration_date);
				formData.append('data_limit', this.data_limit);
				formData.append('use_cold_drive', this.use_cold_drive);

				this.axios.post('/admin/member/modify/', formData
				).then(result => {
					let data = result.data
					if (data.code === 1000) {
						this.$emit('update:visible_modify', false)
						$(".modal_bg").hide()




					}
				}).catch(error => {
					console.log(error)
				})

			}
		},
	};
</script>

<style scoped>

</style>
