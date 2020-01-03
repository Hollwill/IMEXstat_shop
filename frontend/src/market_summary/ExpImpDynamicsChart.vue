<script>
    import { Bar, mixins } from 'vue-chartjs'
    const { reactiveProp } = mixins

    export default {
        extends: Bar,
        mixins: [reactiveProp],
        data() {
            return {
                options: {

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