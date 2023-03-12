<template>
  <div class="project_evaluation text-centre">
    <div v-if="data_for_chart">
      <LineChart
        :chart-data="data_for_chart"
        :chart-options="options_for_chart"
        style="margin: auto;"
        
      />
    </div>
    <div v-else>
      <p>No data to display</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import Chart from 'chart.js/auto';
import { LineChart } from 'vue-chartjs';

export default {
  name: 'EvaluationHistory',
  props: [
    'projectData'
  ],
  data() {
    return {
      chartData: false,
      data_for_chart: {
        labels: [],
        datasets: [{
          label: 'Evaluation History of Last 7 Evaluations',
          data: [],
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options_for_chart:{
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2.2,
        scales: {
          y: {
            max: 10,
            min: 0,
            ticks: {
              stepSize: 1,
              callback: function(value, index, ticks) {
                switch (value) {
                  case 2:
                    return 'Failing';
                  case 4:
                    return 'At Risk';
                  case 6:
                    return 'Showing Symptoms';
                  case 8:
                    return 'Successful';
                  default:
                    return '';
                }
              },
              display: true,
              autoSkip: false,
            }, 
            display: true,
        }
        }
      }
    }
  },
  watch: {
    projectData(){
      this.data_for_chart.labels = [];
      this.data_for_chart.datasets[0].data = [];
      console.log(this.data_for_chart.datasets[0].data)
      let number_counter = 0;
      for ( let evaluation in this.projectData.evaluation_history) {
        if (number_counter < 7) {
          console.log(this.projectData.evaluation_history[evaluation])
          let temp_date = new Date(this.projectData.evaluation_history[evaluation].evaluation_date);
          this.data_for_chart.labels.push(temp_date.toISOString().split('T')[0]);
          const label = this.projectData.evaluation_history[evaluation].evaluation_label;
          switch (label) {
            case 'Failing':
              this.data_for_chart.datasets[0].data.push(2);
              break;
            case 'At Risk':
              this.data_for_chart.datasets[0].data.push(4);
              break;
            case 'Showing Symptoms':
              this.data_for_chart.datasets[0].data.push(6);
              break;
            case 'Successful':
              this.data_for_chart.datasets[0].data.push(8);
              break;
            default:
              this.data_for_chart.datasets[0].data.push(0);
              break;
          }
          number_counter++;
        }else{
          break;
        }
      }
      this.data_for_chart.labels = this.data_for_chart.labels.reverse();
      this.data_for_chart.datasets[0].data = this.data_for_chart.datasets[0].data.reverse();
    }
  },
  methods: {
  },
  mounted() {
    Chart.defaults.font.size = 12;
  }
};

</script>

<style>
  .project_evaluation {
    width: 55%;
    background-color: #f5f5f5;
    border-radius: 15px;
    margin: 15px;
    padding: 5px;
    display: flex;
    flex-direction: column;
    
  }
  
  .scrollable-table {
    max-height: 200px;
    overflow-y: scroll;
  }
  
  .scrollable-date {
    height: 25px; /* set the height of each date element */
    overflow: hidden; /* hide the overflow of long dates */
    white-space: nowrap; /* prevent the date from wrapping */
    text-overflow: ellipsis; /* show an ellipsis if the date overflows */
  }
</style>
