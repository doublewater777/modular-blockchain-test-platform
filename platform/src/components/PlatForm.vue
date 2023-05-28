<template>
  <el-container>
    <el-header>{{ title }}</el-header>
    <el-container>
      <el-aside>
        <el-form
          :model="ruleForm"
          ref="ruleForm"
          label-width="100px"
          class="demo-ruleForm"
        >
          <el-form-item label="哈希函数:" prop="hashAlg">
            <el-radio-group v-model="ruleForm.hashAlg">
              <el-radio label="SM3"></el-radio>
              <el-radio label="Keccak"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="签名函数:">
            <el-radio-group v-model="ruleForm.signAlg">
              <el-radio label="SM2"></el-radio>
              <el-radio label="Secp256k1"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="submitForm()"
              
              >立即生成区块</el-button
            >
          </el-form-item>
        </el-form>
      </el-aside>
      <el-container>
        <el-main>
          <div
            id="myChart"
            style="width: 800px; height: 350px; margin-top: 80px"
          ></div>
          <div
            id="myChart2"
            style="width: 800px; height: 350px; margin-top: 80px"
          ></div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      title: "模块化区块链平台",
      ruleForm: {
        signAlg: "SM3",
        hashAlg: "SM2",
      },
      isloading: false,
      myChart: "",
      myChart2: "",
      Myoption: {
        title: {
          text: "模拟数据",
        },
        tooltip: {},
        legend: {
          data: ["时间/秒"],
        },
        xAxis: {
          data: ["交易吞吐量", "创建区块平均时间", "程序时间"],
        },
        yAxis: {},
        series: [
          {
            name: "时间/秒",
            type: "bar",
            data: [],
          },
        ],
      },
      Myoption2: {
        title: {
          text: "比较",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },
        legend: {
          data: ["交易吞吐量", "创建区块平均时间", "程序时间"],
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: [],
          },
        ],
        yAxis: [
          {
            type: "value",
          },
        ],
        series: [
          {
            name: "交易吞吐量",
            type: "line",
            stack: "总量",
            areaStyle: { normal: {} },
            data: [],
          },
          {
            name: "创建区块平均时间",
            type: "line",
            stack: "总量",
            areaStyle: { normal: {} },
            data: [],
          },
          {
            name: "程序时间",
            type: "line",
            stack: "总量",
            areaStyle: { normal: {} },
            data: [],
          },
        ],
      },
      txData: [],
      BData: [],
      PData: [],
      xAxis: [],
      time: 0,
    };
  },
  methods: {
    submitForm() {
      this.isloading = true;
      
this.myChart.showLoading({
    text: 'loading',
    color: '#4cbbff',
    textColor: '#4cbbff',
    maskColor: 'rgba(0, 0, 0, 0.9',
});
this.myChart2.showLoading({
    text: 'loading',
    color: '#4cbbff',
    textColor: '#4cbbff',
    maskColor: 'rgba(0, 0, 0, 0.9',
});
      axios
        .get("http://127.0.0.1:5000", {
          params: {
            hashAlg: this.ruleForm.hashAlg,
            signAlg: this.ruleForm.signAlg,
          },
        })
        .then((res) => {
          this.isloading = false;
          this.myChart.hideLoading();
          this.myChart.setOption({
            series: [
              {
                name: "时间/秒",
                data: res.data,
              },
            ],
          });
          this.txData.push(res.data[0]);
          this.BData.push(res.data[1]);
          this.PData.push(res.data[2]);
          this.time++;
          this.xAxis.push(this.time);
          this.myChart2.hideLoading();
          this.myChart2.setOption({
            series: [
              {
                name: "交易吞吐量",
                data: this.txData,
              },
              {
                name: "创建区块平均时间",
                data: this.BData,
              },
              {
                name: "程序时间",
                data: this.PData,
              },
            ],
            xAxis: [
              {
                type: "category",
                boundaryGap: false,
                data: this.xAxis,
              },
            ],
          });
        })
        .catch((err) => {
          this.isloading = false;
          console.log(err, "err");
        });
    },
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      this.myChart = this.$echarts.init(document.getElementById("myChart"));
      // 绘制图表

      this.myChart.setOption(this.Myoption);
      this.myChart2 = this.$echarts.init(document.getElementById("myChart2"));
      // 绘制图表

      this.myChart2.setOption(this.Myoption2);
    },
  },
  mounted() {
    this.drawLine();
  },
};
</script>

<style>
.el-main {
  display: flex;
}
</style>