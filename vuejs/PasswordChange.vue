<template>
	<!-- 비밀번호 수정 팝업 -->
	<div class="layer_popup">
		<div class="inner">
			<h3>비밀번호 수정</h3>
			<div class="detail_cont">
				<fieldset class="share_form">
					<legend>비밀번호 수정 설정</legend>
					<div>
						<span class="category"><label for="">현재 비밀번호</label></span>
						<span class="field confirm"><input type="password" id="" style="width: 240px"
														   v-model="currentPwd"
														   :placeholder="$t('messages.guide.current_password')"
														   maxlength="20"/></span>
					</div>
					<div>
						<span class="category"><label for="">새 비밀번호</label></span>
						<span class="field"><input type="password" id="" style="width: 240px" v-model="pwd"
												   :placeholder="$t('messages.guide.password')" maxlength="20"/></span>
					</div>
					<div>
						<span class="category"><label for="">새 비밀번호 확인</label></span>
						<span class="field"><input type="password" id="" style="width: 240px" v-model="confirmPwd"
												   :placeholder="$t('messages.guide.password')" maxlength="20"/></span>
					</div>

				</fieldset>
			</div>
			<div>
				<span class="field error_msg" v-if="errorMessage !== ''"><img
					src="../../../assets/images/component/ico_error.png" alt=""> {{errorMessage}}</span>
			</div>
			<div class="btn_set">
				<div class="right">
					<button type="button" class="btn_basic cancel" @click="closePopup">취소
					</button>
					<!--					<button type="button" class="btn_basic submit" :disabled="disabled">완료</button>-->
					<button type="button" :class="{'btn_basic': btnBasic === true , 'submit':completeInput === true}"
							v-bind:disabled='!isComplete' @click="updatePassword">완료
					</button>
				</div>
			</div>
			<button class="btn_close" @click="closePopup"><img
				src="../../../assets/images/component/btn_popup_close.png" alt="닫기"/></button>
		</div>

	</div>
</template>

<script>
	import {PopupMixin} from "../../popup/PopupMixin";

	export default {
		mixins: [PopupMixin],
		props: {},
		watch: {
			currentPwd: function (value) {
				this.checkForm();
			},
			pwd: function (value) {
				this.checkForm();
			},
			confirmPwd: function (value) {
				this.checkForm();
			}
		},
		data() {
			return {
				currentPwd: '',
				pwd: '',
				confirmPwd: '',
				errorMessage: '',
				btnBasic: false,
				completeInput: false,
				isComplete: false
			}
		},
		created() {


		},

		methods: {
			checkForm() {
				console.log("와치 체크")
				if (this.currentPwd !== '' && this.pwd !== '' && this.confirmPwd !== '' && this.validate() == true) {
					this.isComplete = true;
				} else {
					this.isComplete = false;
				}
			},
			validate() {
				console.log("watch")
				let result = true;
				let message = '';
				let containNumber = /[0-9]/;	// Number
				let containLowerCase = /[a-z]/;	// Lowercase
				let containUpperCase = /[A-Z]/;	// Uppercase
				let containSpChar = /[~!@#$%^&*()_+|<>?:{}]/;	// Special

				if (this.pwd.search(/\s/) > -1) {
					message = this.$t('messages.error.input_minimum_blank');
					result = false;
				} else if (this.pwd.length < 6) {
					message = this.$t('messages.error.input_minimum_six_char');
					result = false;
				} else if (containNumber.test(this.pwd) == false) {
					message = this.$t('messages.error.input_minimum_num');
					result = false;
				} else if (containLowerCase.test(this.pwd) == false) {
					message = this.$t('messages.error.input_minimum_lower_char');
					result = false;
				} else if (containUpperCase.test(this.pwd) == false) {
					message = this.$t('messages.error.input_minimum_upper_char');
					result = false;
				} else if (containSpChar.test(this.pwd) == false) {
					message = this.$t('messages.error.input_minimum_sp_char');
					result = false;
				} else if (this.pwd != this.confirmPwd) {
					message = this.$t('messages.error.not_match_new_confirm_password');
					result = false;
				}

				if (result == false) {
					this.errorMessage = message;
				} else {
					this.errorMessage = '';
				}

				return result;
			},
			updatePassword() {

				console.log("변경", this.isComplete)
				if (this.isComplete == false) {
					return false;
				}

				let valid = this.validate();

				if (valid == false) {
					return false;
				}

				let form = new FormData();
				// form.append('email', this.$cookies.get("payload")['email']);
				form.append('currentPwd', this.currentPwd);
				form.append('pwd', this.pwd);
				form.append('viewType', 'update');
				// form.append('key', this.$cookies.get("payload")['key']);

				this.$http.post('/admin/saveCurrentPassword/', form).then(response => {
					let result = response['data']['result'];
					let code = response['data']['code'];

					if (result == true) {
						this.$vf.showToastMessage(this.dataObject.vm, this.$t('messages.update_password_complete'));
						this.$emit('close');
					} else {
						if (code === -1000 || code === -2006) {
							this.errorMessage = this.$t('messages.error.not_match_new_confirm_password');
						}
					}
				}).catch(error => {

				})
			},
		},
	};
</script>

<style scoped>

</style>
