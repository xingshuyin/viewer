<script setup>
import { onBeforeMount, onBeforeUnmount, onMounted, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import ttime from './components/t-time.vue'
import { Star, ArrowDownBold, ArrowUpBold } from '@element-plus/icons-vue'
// import fs from 'fs'
// import { images } from "./assets/data";
const datas = import.meta.glob('../src/assets/json/**.json');
const datas_keys = Object.keys(datas);
console.log(datas_keys);
const attrs = reactive({
  index: 0,
  set: datas_keys[0],
  data: [],
  max_index: 1,
  random: false,
  adder: false,
  drawer: false,
  data_push: null,
  data_push_name: '',
  data_push_show: false,
})
let adder
onBeforeUnmount(() => {
  clearInterval(adder)
})
onMounted(() => {
  if (localStorage.getItem('index')) attrs.index = localStorage.getItem('index')
  if (localStorage.getItem('set')) attrs.set = localStorage.getItem('set')
  if (localStorage.getItem('max_index')) attrs.max_index = localStorage.getItem('max_index')
})
watch(
  () => attrs.set,
  () => {
    localStorage.setItem('set', attrs.set)
    datas[attrs.set]().then((res) => {
      attrs.data = res['default']
      attrs.index = 0
      attrs.max_index = attrs.data.length - 1
    })
  },
  { immediate: true }
)
watch(() => attrs.index, () => {
  localStorage.setItem('index', attrs.index)
})
watch(() => attrs.max_index, () => {
  localStorage.setItem('max_index', attrs.max_index)
})
watch(
  () => attrs.adder,
  () => {
    if (attrs.adder) {
      adder = setInterval(() => {
        next_img()
      }, 10000)
    } else {
      clearInterval(adder)
    }
    attrs.max_index = attrs.data.length - 1
  }
)
const next_img = () => {
  // console.log(ipcRenderer);
  // ipcRenderer.send('quit')  // TODO: 通信; 想要通信需要现在preload暴露相应对象, 然后调用send方法发送消息
  if (attrs.random) {
    attrs.index = Math.floor(Math.random() * attrs.max_index)
    return
  }
  if (attrs.index < attrs.max_index) {
    attrs.index++
  } else {
    attrs.index = 0
  }
}
const previous_img = () => {
  // console.log(ipcRenderer);
  // ipcRenderer.send('quit')  // TODO: 通信; 想要通信需要现在preload暴露相应对象, 然后调用send方法发送消息
  if (attrs.index > 0) {
    attrs.index--
  } else {
    attrs.index = attrs.max_index
  }
}
const save = () => {
  console.log(attrs.set);
  if (datas_keys.indexOf('./assets/json/' + attrs.data_push_name + '.json') == -1) {
    fs.writeFile('src/renderer/src/assets/json/' + attrs.data_push_name + '.json', attrs.data_push, function (err) {
      if (err) {
        console.log(err)
      } else {
        ElMessage({
          message: '文件已添加到本地',
        })
      }
    })
  } else {
    ElMessage({
      message: '文件已存在',
    })
  }

}
</script>   


<template>
  <div class="m">
    <el-drawer v-model="attrs.drawer" direction="rtl" :with-header="false" size="200px">
      <!-- <el-radio-group v-model="attrs.set" class="tab" size="small">
        <el-radio-button v-for="i, index in datas_keys" :key="i" :label="i">
          {{ i.split("/")[3].split('.')[0] }}
        </el-radio-button>
      </el-radio-group> -->
      <div class="buttons">
        <el-switch v-model="attrs.random" class="switch_random" active-text="随机" />
        <el-switch v-model="attrs.adder" class="adder" active-text="自增" />
        <!-- <el-button type="primary" @click="attrs.data_push_show = !attrs.data_push_show">导入</el-button> -->
      </div>
      <div :style="{ backgroundColor: attrs.set == i ? 'yellow' : '' }" v-for="i, index in datas_keys" :key="i"
        @click="attrs.set = i">
        {{ i.split("/")[3].split('.')[0] }}
      </div>
    </el-drawer>
    <img src="./assets/fc.png" @click="attrs.drawer = !attrs.drawer" class="open-btn">
    <img src="./assets/ll.png" @click="next_img" class="next">
    <img src="./assets/rr.png" @click="previous_img" class="previous">
    <div class="bg" :style="{ backgroundImage: `url(${decodeURI(attrs.data[attrs.index])})` }"></div>
    <div class="switch_index">{{ attrs.index }}</div>
    <!-- <el-slider v-model="attrs.index" :max="attrs.max_index" class="switch_slider" vertical height="60%" /> -->
    <el-image class="viewer" style="width: 100%; height: 100%" :src="decodeURI(attrs.data[attrs.index])" fit="contain"
      lazy @click="1" />
    <el-dialog v-model="attrs.data_push_show" title="导入" width="80%">
      <el-input v-model="attrs.data_push_name" placeholder="名称" />
      <el-input v-model="attrs.data_push" :rows="15" type="textarea" placeholder='[
          "https://50da81cb39dbb6fd8a9b3c7e1e24ab18962b37a2.jpg",
          "https://f8e6ed499389da1ba2728565005209b2.jpeg",
        ]' />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="attrs.data_push_show = false">取消</el-button>
          <el-button type="primary" @click="save">
            添加
          </el-button>
        </span>
      </template>
    </el-dialog>
    <ttime class="time"></ttime>
  </div>
</template>

<style lang="scss">
:root {
  --el-input-bg-color: rgba(0, 0, 0, 0) !important;
}

* {
  margin: 0;
  padding: 0;
  border: 0;
}

.time {
  position: absolute;
  right: 50px;
  top: 10px;
  z-index: 99;
}

.m {
  overflow: hidden;
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: black;

  .bg {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 0;

    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    -webkit-filter: blur(9px);
    -moz-filter: blur(9px);
    -o-filter: blur(9px);
    -ms-filter: blur(9px);
    filter: blur(9px);
  }

  .open-btn {
    position: absolute;
    z-index: 99999990;
    right: 10px;
    top: 10px;
    width: 20px;
    height: 20px;
    transition-duration: 200ms;
  }

  .open-btn:hover {
    transform: scale(2) rotate(360deg);
  }

  .previous,
  .next {
    position: absolute;
    z-index: 99999990;
    top: 50%;
    // transform: translateY(-50%);
    width: 15px;
    height: 15px;
    opacity: 0.5;
    transition-duration: 200ms;
  }

  .previous {
    left: 10px;
  }

  .previous:hover,
  .next:hover {
    transform: scale(2) rotate(360deg);
    opacity: 1;
  }

  .next {
    right: 10px;
  }


  .viewer {
    background-color: rgba(0, 0, 0, 0) !important;

    * {
      background-color: rgba(0, 0, 0, 0) !important;
    }

    .is-loading {
      background-color: rgba(0, 0, 0, 0);
    }
  }

  // .tab {
  //   position: absolute;
  //   z-index: 9999999;
  // }

  // .buttons {
  //   position: absolute;
  //   z-index: 9999999;
  //   right: 0;
  //   display: flex;
  //   flex-direction: column;
  //   align-items: flex-start;
  // }

  .switch_index {
    position: absolute;
    z-index: 9999999;
    right: 5px;
    bottom: 5px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.644);
    border-radius: 5px;

  }

  .link {
    position: absolute;
    z-index: 9999999;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
  }
}

pre::-webkit-scrollbar,
div::-webkit-scrollbar,
textarea::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

pre::-webkit-scrollbar-track,
div::-webkit-scrollbar-track,
textarea::-webkit-scrollbar-track {
  background-color: transparent;
}

pre::-webkit-scrollbar-thumb,
div::-webkit-scrollbar-thumb,
textarea::-webkit-scrollbar-thumb {
  background: #16151575;
  border-radius: 25px;
}
</style>
