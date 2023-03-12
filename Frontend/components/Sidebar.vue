<template>
  <div class="sidebar d-flex justify-content-center flex-column">
    <b-row class="bg-dark" style="margin: 0;">
      <b-col class="sort-by"> 
        <b-dropdown v-model="sortBy" text="Sort By" size="sm">
          <b-dropdown-item value="riskLevel" @click="sortedProjects('riskLevel')">Risk Level</b-dropdown-item>
          <b-dropdown-item value="reverseRiskLevel" @click="sortedProjects('reverseRiskLevel')">Reverse Risk Level</b-dropdown-item>
          <b-dropdown-item value="managerName" @click="sortedProjects('managerName')">Manager Name</b-dropdown-item>
          <b-dropdown-item value="projectName" @click="sortedProjects('projectName')">Project Name</b-dropdown-item>
        </b-dropdown>
      </b-col>
      <b-col class="mt-2 mb-2">
        <b-button variant="primary" class="create-project-button" @click="showCreateProjectForm = true" size="sm"> 
          New Project
        </b-button>
      </b-col>
    </b-row>
    <div class="project-list">
      <div v-for="project in projects" :key="project.projectID" class="project" @click="selectProject(project.project_id)">
        <div class="project-name">{{ project.project_name }}</div>
        <div class="project-risk" :class="project.recent_evaluation_label.replace(' ', '')">{{ project.recent_evaluation_label }}</div>
        <div class="project-manager">Manager - {{ project.project_manager_name }}</div>
      </div>
    </div>
    <b-modal v-model="showCreateProjectForm" title="Create New Project" hide-footer>
      <CreateProjectForm :loading="loading" @form-submitted="hideCreateProjectForm" @project-created="handleProjectCreated" />
    </b-modal>
  </div>
</template>


<script>
import CreateProjectForm from '~/components/CreateProjectForm.vue'
import { BModal, BButton, BDropdown, BDropdownItem, BRow, BCol } from 'bootstrap-vue'

import axios from 'axios'
import { mapGetters } from 'vuex'

export default {
  name: 'Sidebar',
  props: ['projects', 'loading'],
  data() {
    return {
      sortBy: 'Sort By',
      showCreateProjectForm: false
    }
  },
  
  computed: {
  },

methods: {
  selectProject(project_id) {
    this.$root.$refs.Dashboard.selectProject(project_id);
  },

  sortedProjects(c) {
      console.log(this.sortBy);
      console.log(c);
      if (c === 'reverseRiskLevel') {
        return this.projects.sort((a, b) => {
          const riskLevelOrder = {
            'Successful': 0,
            'Showing Symptoms': 1,
            'At Risk': 2,
            'Failing': 3
          }
          return riskLevelOrder[a.recent_evaluation_label] - riskLevelOrder[b.recent_evaluation_label]
        })
      } else if (c === 'riskLevel') {
        return this.projects.sort((a, b) => {
          const riskLevelOrder = {
            'Successful': 0,
            'Showing Symptoms': 1,
            'At Risk': 2,
            'Failing': 3
          }
          return riskLevelOrder[b.recent_evaluation_label] - riskLevelOrder[a.recent_evaluation_label]
        })
      } else if (c === 'managerName') {
        return this.projects.sort((a, b) => {
          return a.project_manager_name.localeCompare(b.project_manager_name)
        })
      } else if (c === 'projectName') {
        return this.projects.sort((a, b) => {
          return a.project_name.localeCompare(b.project_name)
        })
      }
      return this.projects
    },
  handleProjectCreated(project) {
    // Add the new project to the list  -- NOT SURE IF WE ADD PROJECT TO LIST AFTER CREATION OR IT SENDS TO BACKEND THEN UPDATES THE LOOP
    console.log('THIS IS WORKING')

    // Close the create project form
    this.showCreateProjectForm = false
  },
  hideCreateProjectForm(){
    this.showCreateProjectForm = false
  }
}
}
</script>

<style>
  .sidebar {
    width: 20%;
    background-color: #f5f5f5;
    box-sizing: border-box;
    max-height: 100%;
    min-height: 100%;
    height: 90vh;

  }
  .project-list {
    overflow-y: scroll;
    padding: 16px;
    height: 100%;
    width: 100%;
  }

  .sort-by {
    margin: auto;
  }

  .project {
    display: flex;
    flex-direction: column;
    margin-bottom: 16px;
    padding: 8px;
    border-radius: 4px;
    box-shadow: 0 2px 2px #ccc;
    cursor: pointer;
  }

  .project:hover {
    background-color: #eee;
  }

  .project-name {
    font-size: 16px;
    font-weight: bold;
  }

  .project-risk {
    font-size: 12px;
    color: #fff;
    text-align: center;
    padding: 4px 8px;
    border-radius: 4px;
  }

  .Failing{
    background-color: #ff4d4f;
  }

  .AtRisk {
    background-color: #faad14;
  }

  .ShowingSymptoms{
    background-color: #8314fa;
  }

  .Successful {
    background-color: #52c41a;
  }

  .project-manager {
    font-size: 12px;
  }
</style>
