<template>
	<body class="none_gnb">
	<div id="member_container">
		<section id="member_info">
			<h1><img src="../../assets/images/layout/logo.svg" alt="AOS DataShare"/></h1>
			<div class="member_form">
				<fieldset>
					<legend>로그인정보 입력</legend>
					<h2>로그인</h2>
					<p class="field">
						<label for="memberId">ID(email)</label>
						<img src="../../assets/images/member/bullet_user.png" alt="ID" class="ico">
						<input type="text" placeholder="아이디를 입력해주세요" id="memberId" v-model="email"
							   @keyup="keyUpEmail($event)"/>
					</p>
					<p class="error_msg" v-show="idErrorMessage !==''">
						<img src="../../assets/images/component/ico_error.png" alt=""> {{ idErrorMessage }}
					</p>
					<p class="field">
						<label for="memberId">비밀번호 입력</label>
						<img src="../../assets/images/member/bullet_lock.png" alt="비밀번호" class="ico">
						<input type="password" placeholder="비밀번호를 입력해주세요" id="memberPass" v-model="password"
							   @keyup="keyUpPassword($event)"/>
					</p>
					<p class="error_msg" v-show="pwErrorMessage !==''">
						{{ pwErrorMessage }}
					</p>
					<p class="save_login_info">
						<label><input type="checkbox"/>기억하기</label>
					</p>
					<p class="select_language">
					<span class="basic_select selectbox_ui">
						<b class="selected_txt" v-if="language == 'ko_KR'">한국어</b>
						<b class="selected_txt" v-if="language == 'ja_JP'">일본어</b>
						<select title="상태 설정" v-model="language" @change="changeLanguage">
							<option value="ko_KR">한국어</option>
							<option value="ja_JP">일본어</option>
						</select>
					</span>
					</p>
					<p class="btn_set">
						<button type="button" @click="login">확인</button>
					</p>
					<p class="find_password"><a href="#">다른 계정으로 로그인</a></p>
					<p class="robot"><img src="../../assets//images/member/img_captcha.png" alt="CaptCha"></p>
				</fieldset>
			</div>
			<p class="copyright">Copyright©2020 AOS DataShare</p>
		</section>
	</div>

	<!-- 모달 배경 -->
	</body>

</template>

<script>
	export default {
		name: "Login.vue",
		data() {
			return {
				email: '',
				password: '',
				memorize: false,
				language: 'default',
				status: 0,
				idErrorMessage: '',
				pwErrorMessage: ''
			}
		},
		created() {
			this.language = this.$i18n.locale
			this.email = this.$cookies.get('loginEmail')
			if (this.email != '')
				this.memorize = true
			this.keyUpEmail()
		},
		mounted() {
			//셀렉트박스 UI
			jQuery(".selectbox_ui").each(function () {
				initSelectBox(jQuery(this)) //비동기로 셀렉트 박스를 만들었을 경우 initSelectBox(jQuery("#아이디")) 로 실행시켜줘야 함
			})
		},
		methods: {
			// 이메일 체크
			login() {

				// 비밀번호가 입력되어 있는지 다시 한번 체크
				if (this.password === '') {
					this.pwErrorMessage = '비밀번호를 입력해주세요.'
					return
				}

				let qs = require('qs');
				let vm = this
				this.axios.post('/admin/login/',
					qs.stringify({
						email: this.email,
						pw: this.password,
						language: this.language
					})
				).then(result => {
					let data = result.data
					if (data.code === 1000) {
						vm.moveMain(data)
					}


				}).catch(error => {
					console.log(error)
				})
			},
			keyUpEmail(e) {
				if (this.email === '') {
					this.idErrorMessage = '아이디를 입력해주세요.'
					return
				}
				let re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
				if (!re.test(this.email)) {
					this.idErrorMessage = '유효한 email을 입력하세요.'
					return
				}
				this.idErrorMessage = ''
			},
			keyUpPassword(e) {
				if (this.password === '') {
					this.pwErrorMessage = '비밀번호를 입력해주세요.'
					return
				}
				this.pwErrorMessage = ''

			},

			moveMain(data) {
				this.$router.push({path: '/main', query: {linkId: this.linkId}})
			},
			changeLanguage() {
				this.$i18n.locale = this.language
			},
		},
	}
</script>

<style scoped>

</style>
