<template>
    <div id="exp-imp-dynamics">
        <exp-imp-dynamics-chart v-if="show_chart" :chart-data="chartdata"/>

        <p v-for="data in tabledata" v-bind:key="data.id">
            {{ data.labelList }}, {{ data.impData }}, {{ data.expData }}
        </p>
    </div>
</template>

<script>
    import { HTTP } from '../http-common'
    import ExpImpDynamicsChart from "./ExpImpDynamicsChart";
    import moment from 'moment'

    export default {
        name: "ExpImpDynamics",
        components: {
            ExpImpDynamicsChart
        },
        props: ['date', 'params', 'interval'],
        data() {
            return {
                show_chart: false,
                chartdata: {
                    labels: null,
                    datasets: [
                        {
                            label: 'Импорт',
                            backgroundColor: '#FFF839',
                            data: null
                        },
                        {
                            label: 'Экспорт',
                            backgroundColor: '#1221FF',
                            data: null
                        }
                    ]
                },
                table: {
                    labels: null,
                    exp: {
                        data: null,
                        dynamics: null
                    },
                    imp: {
                        data: null,
                        dynamics: null
                    }
                }
            }
        },
        computed: {
            tabledata: function () {
                if (this.show_chart) {
                    let iterList = [];
                    for (let i = 0; i < this.chartdata.labels.length; i++) {
                        iterList.push(
                            {
                                labelList: this.chartdata.labels[i],
                                impData: this.chartdata.datasets[0].data[i],
                                expData: this.chartdata.datasets[1].data[i]
                            }
                        )
                    }
                    return iterList
                } else {
                    return null
                }
            }
        },
        methods: {
            recount(date_to = this.date.to , date_from = this.date.from ) {
                HTTP.get('statistic/exp_imp_dynamics/', {
                    params: {
                        'date_from': date_from,
                        'date_to': date_to,
                        'interval': this.interval
                    }
                })
                    .then(response => {
                        if (this.params === 'stoim') {
                            this.chartdata = response.data.chart.cost.chartdata
                        } else {
                            this.chartdata = response.data.chart.netto.chartdata
                        }
                        this.show_chart = true
                    })
            }
        },
        mounted() {
            let date_to = new Date();
            let date_from = new Date(date_to.getTime());
            date_from.setFullYear(date_from.getFullYear() - 3);
            this.recount(moment(date_to).format("YYYY-MM"), moment(date_from).format("YYYY-MM"));
        }

    }
</script>

<style scoped>
#exp-imp-dynamics {
    margin-top: 15px;
}
</style>