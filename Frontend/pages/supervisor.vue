<template>
    <div class="main-content">
      <div class="fill">
        <div class="text-center">
          <h1 style="font-weight:bold">
            <b-icon-people-fill></b-icon-people-fill> Team Management
          </h1>
        </div>
        <div class="text-center">
          <AssignedManagers style="display: inline-block; vertical-align: top"
          :assigned="assigned"
          :unassigned="unassigned"></AssignedManagers>
          <UnassignedManagers style="display: inline-block; vertical-align: top"
          :assigned="assigned"
          :unassigned="unassigned"></UnassignedManagers>
        </div>
      </div>
    </div>
</template>

<script>
  import axios from 'axios'

  import { BIconPeopleFill } from 'bootstrap-vue'

  import AssignedManagers from '~/components/AssignedManagers.vue'
  import UnassignedManagers from '~/components/UnassignedManagers.vue'

  export default {
    name: 'supervisor',
    layout: 'default',
    middleware: ['supervisor'],
    components: {
      AssignedManagers,
      UnassignedManagers
    },

    data() {
      return {
        assigned: [],
        unassigned: []
      }
    },

    created() {
        this.$root.$refs.Supervisor = this;
    },

    methods: {
      logout() {
        this.$auth.logout()
        this.$router.push('/')
      }
    },

    mounted() {
      const params = new URLSearchParams();
      params.append('supervisor_id', this.$auth.user.user_id);
      params.append('server_token', '0');
      // console.log(params.toString()); // add this line
      axios.post('http://localhost:5555/get_all_pm', params, {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded', 
          'x-access-token': this.$auth.strategy.token.get().substr(7)
        }
      })
      .then(response => {
        this.assigned = response.data;
      })
      .catch(error => {
        // console.log(error);
      });
      
      const body = {
        "server_token": 0,
        "substring": ""
      };
      
      // This needs to be the a call to the endpoint to search for users who are
      // specifically not assigned to the supervisor instead of all users.
      axios.post('http://localhost:5555/get_unassigned_pm', params, {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded', 
          'x-access-token': this.$auth.strategy.token.get().substr(7)
        }
      }).then(response => {
          this.unassigned = response.data;
      });
    }
  }
</script>

<style>
.fill {
  max-height: 90vh;
  height: 90vh;
  width: 100%;
  background-color: lightgray;
}

.aaaa {
  background-color: darkgray;
}
</style>