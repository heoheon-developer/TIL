<template>
	<span class="input_box">
		<button type="button" class="active_add" @click="clickAddActivations">동작추가</button>
		<span class="keyword" v-for="(row, index) in tags">
			{{ row['name'] }}
			<button type="button" class="btn_delete" @click="clickDel(index)"><span>삭제</span></button>
		</span>
		<!--<span class="keyword">
			파일 및 폴더 추가
			<button type="button" class="btn_delete"><span>삭제</span></button>
		</span>
		<span class="keyword">
			파일 및 폴더 다운로드
			<button type="button" class="btn_delete"><span>삭제</span></button>
		</span>
		<span class="keyword">
			파일 및 폴더 완전 삭제
			<button type="button" class="btn_delete"><span>삭제</span></button>
		</span>-->
	</span>
</template>

<script>
import Activations from '@/components/popup/Activations';

export default {
	name: 'InputActivationTags',
	props: {
		value: {
			code: String,
			tagName: String
		},

		category: {
			type: String,
			default: 'report'
		},
	},
	data() {
		return {
			tags: [...this.value],
		}
	},
	watch: {
		value() {
			this.tags = [...this.value];

		},
		'findRows.length': function () {
			this.showList = this.isAbleToShowList();
		},
	},
	methods: {
		clickAddActivations() {
			this.$modal.show(Activations,{
				vm: this,
				category: this.$props.category
			})
		},
		clickDel(index) {
			this.tags.splice(index, 1);
		},
		addTags(rows) {
			this.tags = rows;
			this.$emit("update:tags", this.tags);
			this.$emit("input", this.tags);
		}

	}
};
</script>

<style scoped>

</style>
