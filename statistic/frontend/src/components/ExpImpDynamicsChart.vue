
<script>
    import { Bar, mixins } from 'vue-chartjs'
    const { reactiveProp } = mixins

    export default {
        extends: Bar,
        mixins: [reactiveProp],
        props: ['chartData'],
        data() {
            return {
                options: {
                    responsive: true
                }
            }
        },
        mounted() {
            this.renderChart(this.chartData, this.options)
        }
    }
</script>

<style scoped>
* {
    width: 500px;
    height: 500px;
}
</style>