import ConnectedDevice from '../../views/connected_device/connected_device.vue'

export default [
  {
    path: '/connected_device/:device_name',
    name: 'device',
    component: ConnectedDevice
  },
]
