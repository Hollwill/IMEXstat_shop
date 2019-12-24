
<script>
    import { Pie, mixins } from 'vue-chartjs'
    const { reactiveProp } = mixins

    export default {
        extends: Pie,
        mixins: [reactiveProp],
        props: ['chartData'],
        name: "TurnoverStructurePieChart",
        mounted() {
            this.renderChart(this.chartData, {maintainAspectRatio: false, onClick:this.handle})
        },
        methods: {
          handle (point, event) {
            const item = event[0]
            this.$emit('on-receive', this.chartData.labels[item._index])
          }
        }

    }
</script>

<style scoped>
* {
    width: 500px;
    height: 500px;
}
</style>