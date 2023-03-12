<template>
    <div class="pm-list text-center" style="position:relative;">
        <div class="project-name">
          Add more people
        </div>
        <b-form-input
            id="search"
            type="search"
            placeholder="Search for someone..."
            v-model="substring">
        </b-form-input>
        <b-table
          responsive
          hover
          :items="unassigned.filter(this.doesContain)"
          :fields="fields"
          thead-class="d-none"
          class="pm-list-table"
          sticky-header="250px">
          <template #cell(email)="data">
            <div style="color: gray; font-size: 12px; text-align: left" v-text="data.item.email"></div>
          </template>
          <template #cell(user_id)="data">
            <b-icon-person-plus-fill class="clickable" @click="assignManager(data.item)"></b-icon-person-plus-fill>
          </template>
        </b-table>
        <div v-if="unassigned.filter(this.doesContain).length == 0" class="no-match">
          <b-icon-x-circle></b-icon-x-circle> No matches.
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import { BIconPersonPlusFill, BIconInfoCircle } from 'bootstrap-vue'


export default {
  name: 'UnassignedManagers',
  props: ['assigned', 'unassigned'],

  data() {
    return {
      fields: ['username', 'email', 'user_id'],
      substring: ''
    }
  },

  methods: {
    doesContain(user) {
      return (user.username.includes(this.substring)) || (user.email.includes(this.substring));
    },

    assignManager(user) {
      const params = new URLSearchParams();
      params.append('supervisor_id', this.$auth.user.user_id);
      params.append('project_id', user.user_id);
      // params.append('server_token', '0');
      axios.post('http://localhost:5555/assign_pm', params, {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded', 
          'x-access-token': this.$auth.strategy.token.get().substr(7)
        }
      })
      .then(response => {
        for (var i=0; i < this.unassigned.length; i++) {
          if (this.unassigned[i].user_id == user.user_id) {
            this.unassigned.splice(i, 1);
            break;
          }
        }
        this.assigned.push(user);
      })
      .catch(error => {
        // console.log(error);
      });
    }
  },
}
</script>

<style>

  .clickable {
    font-size: 20px;
  }

  .clickable:hover {
    cursor: pointer;
    color: darkslategrey;
  }

  .pm-list {
    width: 25%;
    background-color: #f5f5f5;
    border-radius: 15px;
    margin: 15px;
    padding: 5px;
    height: 358px;
  }

  .pm-list-footer {
    position: absolute;
    bottom:5px;
    width:100%;
  }

  .project-name {
    font-size: 16px;
    font-weight: bold;
  }

  .pm-list-table {
    font-size: 14px;
  }

  .no-match {
    color: gray;
    font-size: 16px;
  }
</style>