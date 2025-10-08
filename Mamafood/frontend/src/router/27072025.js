import { createRouter, createWebHistory } from 'vue-router';

// Seiten und Komponenten importieren
import Home from '../components/pages/Home.vue'
import Signup from '../components/pages/Signup.vue';
import Login from "../components/pages/Login.vue";
import FoodManagement from "../components/pages/FoodManagement.vue";
import Profile from "../components/pages/Profile.vue";
import MyDishes from "../components/MyDishes.vue";
import EmailConfirmation from "../components/pages/EmailConfirmation.vue";
import ForgetPassword from "../components/pages/ForgetPassword.vue";
import AccountVerification from "../components/pages/AccountVerification.vue";
import UserDashboard from "../components/pages/UserDashboard.vue";
import ResetPassword from "../components/pages/ResetPassword.vue";
import ChefSignup from "../components/pages/ChefSignup.vue";
import ChefPanel from "../components/ChefPanel.vue";
import ChefInfo from "../components/pages/ChefInfo.vue";
import WelcomSite from '../components/pages/WelcomSite.vue';
import ChefPage from '../components/pages/ChefPage.vue';
const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { showNav: true }
  },
   {
    path: '/',
    name: 'WelcomeSite',
    component: WelcomSite,
    meta: { showNav: true }
  },
  {
    path: '/chef/:id',
    name: 'chef',
    component: ChefPage,
    meta: { requiresAuth: true, showNav: true },
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: Signup,
    meta: { showNav: true }
  },
  {
    path: '/email-confirmation',
    name: 'email-confirmation',
    component: EmailConfirmation
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { showNav: true }
  },
{
  path: '/userdashboard',
  name: 'UserDashboard',
  component: UserDashboard,
  meta: { requiresAuth: true, showNav: true },
  children: [
    {
      path: '',
      name: 'UserDashboardHome',
      component: WelcomSite  // Re-use the imported Home component
    },
  ]
},
  {
    path: '/auth/account-verify',
    name: 'AccountVerification',
    component: AccountVerification
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgetPassword,
    meta: { showNav: true }
  },
  {
    path: '/chefsignup',
    name: 'ChefSignup',
    component: ChefSignup
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPassword
  },
  {
    path: '/chef',
    component: ChefPanel,
    meta: { requiresAuth: true, showNav: true },
    children: [
      { path: '', redirect: '/chef/mydishes' }, // Redirect /chef to /chef/mydishes
      { path: 'mydishes', name: 'MyDishes', component: MyDishes }, 
      { path: 'profile', name: 'Profile', component: Profile },
      { path: 'chefinfo', name: 'ChefInfo', component: ChefInfo },
      { path: 'food-management', name: 'FoodManagement', component: FoodManagement }
    ]
  },
  {
    path: '/chefinfo',
    name: 'ChefInfo',
    component: ChefInfo,
    meta: { showNav: true },
  },
  {
    path: '/:catchAll(.*)', 
    redirect: '/chef'
  }
  
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Auth-Guard für geschützte Seiten
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
