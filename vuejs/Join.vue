<template>
	<div id="member_container">
		<h1><img src="@/assets/images/layout/logo.svg" alt="AOS DataShare" /></h1>
		<section id="member_info">
			<div class="member_form">
				<h2>{{$t("join.title")}}</h2>
				<p class="msg"><strong>{{email}}</strong>{{$t("join.text_1")}}</p>
				<fieldset>
					<legend>사용자 등록 정보 입력</legend>
					<p class="field">
						<label for="memberId">{{$t("join.id")}}</label>
						<input type="text" :placeholder="email" id="" disabled :maxlength="100"/>
					</p>
					<p class="error_msg" v-show="emailErrorMsg != ''"><img src="@/assets/images/component/ico_error.png" alt=""> {{emailErrorMsg}} </p>

                    <p class="field">
						<label for="memberName">{{$t("join.name")}}<b>*</b> </label>
						<input type="text" :placeholder="$t('join.placeholderName')" id="memberName" v-model="name" :maxlength="50" @keyup="keyUpName($event)"/>
					</p>
					<p class="error_msg" v-show="nameErrorMsg != ''"><img src="@/assets/images/component/ico_error.png" alt=""> {{nameErrorMsg}}</p>

					<p class="field">
						<label for="memberPass">{{$t("join.pw")}}<b>*</b> </label>
						<input type="password" :placeholder="$t('join.placeholderPw')" id="memberPass" @keyup="keyUpPw($event)" v-model="pw"/>
					</p>
					<p class="error_msg" v-show="pwErrorMsg != ''"><img src="@/assets/images/component/ico_error.png" alt=""> {{pwErrorMsg}}</p>

					<p class="field">
						<label for="memberRePass">{{$t("join.pwConfirm")}}<b>*</b> </label>
						<input type="password" :placeholder="$t('join.placeholderPwConfirm')" id="memberRePass" @keyup="keyUpPwConfirm($event)" v-model="pwConfirm"/>
					</p>
					<p class="error_msg" v-show="pwConfirmErrorMsg != ''"><img src="@/assets/images/component/ico_error.png" alt=""> {{pwConfirmErrorMsg}}</p>

					<p class="field">
						<label for="memberPart">{{$t("join.pwConfirm")}} </label>
						<input type="text" :placeholder="$t('join.placeholderDepartmentName')" id="memberPart" v-model="departmentName" :maxlength="50"/>
					</p>

					<p class="field">
						<label><input type="checkbox" v-model="termsChk" :class="{'error': termsError}"/> {{$t('join.terms_1')}} <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {{$t('join.terms_2')}} </label>
					</p>
					<p class="btn_set"><button type="button" @click="clickConfirm">{{$t('join.insert')}}</button></p>
					<p class="find_password">
						{{$t('join.alreadyJoin')}} <a href="#" @click="clickLogin">{{$t('join.login')}}</a>
					</p>
				</fieldset>
			</div>
		</section>
		<p class="copyright">Copyright©2020 AOS DataShare</p>
	</div>
</template>

<script>
	export default {
		name: "Join",
		data(){
			return{
				email: '',
				name: '',
				pw: '',
				pwConfirm: '',
				departmentName: '',
				termsChk: false,

				emailErrorMsg: '',
				pwErrorMsg: '',
				pwConfirmErrorMsg: '',
				nameErrorMsg: '',
				termsError: false
			}
		},

		methods:{

			valueCheck(){

				let result = true
				this.nameErrorMsg = ''
				this.pwErrorMsg = ''
				this.pwConfirmErrorMsg = ''
				this.termsError = ''

				if(this.name == ''){
					this.nameErrorMsg = this.$t('join.errorMsg_1')
					result = false
				}

				let regx = /(?=.*[A-Z])((?=.*[\W]))/
				if(!regx.test(this.pw)){
					this.pwErrorMsg = this.$t('join.errorMsg_2')
					result = false
				}

				if(this.pw.length < 8){
					this.pwErrorMsg = this.$t('join.errorMsg_3')
					result = false
				}

				if(this.pw == ''){
					this.pwErrorMsg = this.$t('join.errorMsg_1')
					result = false
				}

				if(this.pw != this.pwConfirm){
					this.pwConfirmErrorMsg = this.$t('join.errorMsg_4')
					result = false
				}

				if(this.pwConfirm == ''){
					this.pwConfirmErrorMsg = this.$t('join.errorMsg_1')
					result = false
				}

				if(!this.termsChk){
					this.termsError = true
					result = false
				}

				return result

			},

			keyUpName(e){
				if(e.keyCode == 13)
					this.clickConfirm()
			},

			keyUpPw(e){
				if(e.keyCode == 13)
					this.clickConfirm()
			},

			keyUpPwConfirm(e){
				if(e.keyCode == 13)
					this.clickConfirm()
			},

			clickConfirm(){

				if(!this.valueCheck())
					return

				this.$axios.post('/user/joinUser/',
					require('qs').stringify({
						email: this.email,
						pw: this.pw,
						name: this.name,
						departmentName: this.departmentName,
						link: this.$route.query.link
					})
				).then(result => {

					let data = result.data
					console.log(result)
					if(data.code > 0){
						this.$router.push({
							name: 'JoinSuccess',
							query: {'email': this.email, 'name': this.name, 'department': this.department}
						})
					}else{
						alert('존재하지 않는 유저입니다.')
					}
				}).catch(error => {
					console.log(error)
				})

			},

			clickLogin(){
				this.$router.push({name: 'Login'})
			}

		},

		mounted() {
			let link = this.$route.query.link

			if(!link){
				alert('이미 만료되었거나 잘못된 링크입니다.')
				this.$router.push({name: 'Login'})
				return
			}


			this.$axios.post('/user/linkCheck/',
				require('qs').stringify({
					link: link,
					linkType: 'INVITE'
				})
			).then(result => {

				let data = result.data
				if(data.code < 0){
					alert('이미 만료되었거나 잘못된 링크입니다.')
					this.$router.push({name: 'Login'})
					return
				}

				this.email = data.data

			}).catch(error => {
				console.log(error)
			})
		}
	}
</script>

<style scoped>

</style>