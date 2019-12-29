<template>
  <div class="turnover-structure">
    <h1>Структура товарооборота во внешнй торговли России</h1>
    <div class="d-table">
      <div class="d-tr" v-for="(label, index) in table_data.labels" :key="index">
        <div class="d-td div-as-button" @click="extendTnved(label)">{{label}}</div>
        <div class="d-td">{{table_data.netto[0][index]}}</div>
        <div class="d-td">{{table_data.netto[1][index]}}</div>
        <div class="d-td">{{table_data.cost[0][index]}}</div>
        <div class="d-td">{{table_data.cost[1][index]}}</div>
      </div>
    </div>
<!--    "#xxxxxx".replace(/x/g, y=>(Math.random()*16|0).toString(16))-->
    <turnover-structure-pie-chart
            @on-receive="extendTnved"
            :chart-data="chart_data"
    ></turnover-structure-pie-chart>
    <button @click="getMore" v-if="table_data">получить еще</button>
  </div>
</template>

<script>
    import { HTTP } from '../http-common'
    import moment from 'moment'
    import TurnoverStructurePieChart from "./TurnoverStructurePieChart";

    export default {
        name: "TurnoverStructure",
        components: {
            TurnoverStructurePieChart
        },
        props: ['date', 'interval', 'params', 'category'],
        data() {
            return {
                table_data: {
                    labels: [],
                    netto: [[], []],
                    cost: [[], []],
                },
                chart_data: {
                    labels: [],
                    datasets: [
                        {
                            label: "",
                            data: []
                        }
                    ]
                },
                startdata: 0,
                dataLength: 12,
            };
        },
        methods: {
            recount(tnved, date_to = this.date.to, date_from = this.date.from,) {
                let def_date_to = moment(new Date()).format("YYYY-MM");

                let def_date_from = new Date(new Date().getTime());
                def_date_from.setMonth(def_date_from.getMonth() - 6);
                def_date_from = moment(def_date_from).format("YYYY-MM");

                HTTP.get('statistic/turnover_structure/', {
                    params: {
                        'date_from': date_from && date_to ? date_from : def_date_from,
                        'date_to': date_from && date_to ? date_to : def_date_to,
                        'interval': this.interval,
                        'category': this.category,
                        'start': this.startdata,
                        'length': this.dataLength,
                        'tnved': tnved

                    }
                })
                    .then(response => {
                        this.table_data.labels.push.apply(this.table_data.labels, response.data.labels)
                        this.table_data.netto[0].push.apply(this.table_data.netto[0], response.data.netto[0])
                        this.table_data.netto[1].push.apply(this.table_data.netto[1], response.data.netto[1])
                        this.table_data.cost[0].push.apply(this.table_data.cost[0], response.data.cost[0])
                        this.table_data.cost[1].push.apply(this.table_data.cost[1], response.data.cost[1])
                        this.chart_data = {
                                            labels: this.table_data.labels,
                                            datasets: [
                                                {
                                                    label: "",
                                                    data: this.table_data.netto[0]
                                                }
                                            ]
                                        }
                    })
            },
            extendTnved(label) {
                this.clear()
                this.recount(label)

            },
            clear() {
                this.table_data.labels = [];
                this.table_data.netto = [[], []];
                this.table_data.cost = [[], []];
                this.startdata = 0

            },
            getMore() {
                this.startdata = this.startdata + 12;
                this.recount()
            },

        },
        created() {
            this.$eventHub.$on('recount', this.recount)
            this.$eventHub.$on('recount', this.clear)
        },
        beforeDestroy(){
            this.$eventHub.$off('recount');
        },
        mounted() {
            let date_to = new Date();
            let date_from = new Date(date_to.getTime());
            date_from.setMonth(date_from.getMonth() - 6);
            this.recount(null, moment(date_to).format("YYYY-MM"), moment(date_from).format("YYYY-MM"))
        },

    }
</script>

<style scoped>

</style>