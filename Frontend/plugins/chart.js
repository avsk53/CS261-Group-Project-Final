import Vue from 'vue'
import { Bar, Line, Doughnut, Pie } from 'vue-chartjs'
import { 
    Chart as ChartJS, 
    Title, 
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    LineElemnt,
    PointElement,
    ArcElement,
} from 'chart.js'

// ChartJS.register(
//     Title,
//     Tooltip,
//     Legend,
//     BarElement,
//     CategoryScale,
//     LinearScale,
//     LineElement,
//     PointElement,
//     ArcElement,
// )

Vue.component('BarChart', {
    extends: Bar,
})
Vue.component('LineChart', {
    extends: Line,
})
Vue.component('DoughnutChart', {
    extends: Doughnut,
})
Vue.component('PieChart', {
    extends: Pie,
})