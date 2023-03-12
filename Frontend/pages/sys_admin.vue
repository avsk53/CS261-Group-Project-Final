<template>
      <div class="main-content">
        <CreateUserAccount/>
      </div>
  </template>
  
  <script>
    import NavBar from '~/components/NavBar.vue'
  

    export default {
      name: 'sys_admin',
      layout: 'default',
      middleware: ['admin'], 
      components: {
        NavBar
      },
      methods: {
        logout() {
          this.$auth.logout()
          this.$router.push('/')
        }
      }
    }
  </script>
  
  <style>
  .dashboard {
    display: flex;
    max-height: 85vh;
  }
  
  .main-content {
    flex: 1;
    /* your main content styles here */
  }
  </style>