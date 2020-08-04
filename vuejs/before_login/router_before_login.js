import BeforeLoginLayout from '../../views/before_login/BeforeLoginLayout'
import login from '../../views/before_login/Login.vue'
import findPassword from '../../views/before_login/FindPassword.vue'
import resetPasswordForm from '../../views/before_login/ResetPasswordForm.vue'
import memberJoinForm from '../../views/before_login/MemberJoinForm.vue'
import authen from '../../views/before_login/Authen.vue'

export default [

    {
        path: '/before_login',
        component: BeforeLoginLayout,
        children: [
            {
                path: 'login',
                component: login
            },
            {
                path: 'findPassword',
                component: findPassword
            },
            {
                path: 'resetPasswordForm',
                component: resetPasswordForm
            },
            {
                path: 'memberJoinForm',
                component: memberJoinForm
            },
            {
                path: 'authen',
                component: authen,
                name: 'authen',
                props: true
            },
        ]
    }
]