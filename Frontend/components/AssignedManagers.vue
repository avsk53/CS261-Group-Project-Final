<template>
    <div class="pm-list text-center" style="position:relative;">
        <div class="project-name">
          Your team
        </div>
        <b-table
          responsive
          sticky-header="288px"
          hover
          :items="assigned"
          :fields="fields"
          thead-class="d-none"
          class="pm-list-table">
          <template #cell(email)="data">
            <div style="color: gray; font-size: 12px; text-align: left" v-text="data.item.email"></div>
          </template>
          <template #cell(user_id)="data">
            <b-icon-person-x-fill class="clickable" @click="unassignManager(data.item)"></b-icon-person-x-fill>
          </template>
        </b-table>
    </div>
</template>

<script>

import axios from 'axios'

import { BIconInfoCircle, BIconPersonXFill } from 'bootstrap-vue'

export default {
  name: 'AssignedManagers',
  props: ['assigned', 'unassigned'],
  data() {
    return {
      fields: ['username', 'email', 'user_id']
    }
  },

  methods: {
    unassignManager(user) {
      const params = new URLSearchParams();
      params.append('supervisor_id', this.$auth.user.user_id);
      params.append('project_id', user.user_id);
      // params.append('server_token', '0');
      axios.post('http://localhost:5555/unassign_pm', params, {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded', 
          'x-access-token': this.$auth.strategy.token.get().substr(7)
        }
      })
      .then(response => {
        for (var i=0; i < this.assigned.length; i++) {
          if (this.assigned[i].user_id == user.user_id) {
            this.assigned.splice(i, 1);
            break;
          }
        }
        this.unassigned.push(user);
      })
      .catch(error => {
        // console.log(error);
      });
    }
  }
}
</script>
