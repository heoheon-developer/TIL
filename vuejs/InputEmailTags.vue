<template>
	<!--<div>-->
	<div @click="focusNewTag()" v-click-outside="onClickOutside"
	:class="{
	'read-only': readOnly,
	'tag-wrapper--active': isInputActive,
	}"
	class="tag-wrapper">
		<span class="field email_eidt">
			<span v-for="(row, index) in innerTags" :key="index" class="keyword input-tag" :class="{'error': row.valid == false}">
				<i :class="setIconType(row)"></i> <!--개인 아이콘 -->
				<span :title="row.message">{{ row.tagName }}</span>
				<button type="button" class="btn_delete" @click="remove(index)"><span>삭제</span></button>
			</span>
			<span class="email">
				<input type="text" placeholder="이메일 주소 입력" v-if="!readOnly && !isLimit"
					ref="inputTag"
					:placeholder="'입력'"
					v-model="newTag"
					v-on:keydown.delete.stop="removeLastTag"
					v-on:keydown.stop="addNew"
					v-on:focus="handleInputFocus"
					class="new-tag"
					maxlength="100"
					style="width: unset;"
					@keydown.up.prevent="keyUp"
					@keydown.down.prevent="keyDown"
					@input="inputChange"
				>
				<!-- 자동완성 목록 -->
				<ul class="email" :class="{'show': this.showList, 'hide':  !this.showList}">
					<li v-for="(row, index) in findRows" :class="{'cursor': cursor == index}" @click="selectedRow(row)">
						<i :class="setIconType(row)"></i> {{ row['name'] + (row['email'] ? '(' + row['email'] +  ')' : '') }}
					</li>
				</ul>
			</span>
		</span>
	</div>
</template>

<script>
	const validators = {
		email: new RegExp(
			/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
		),
		url: new RegExp(
			/^(https?|ftp|rmtp|mms):\/\/(([A-Z0-9][A-Z0-9_-]*)(\.[A-Z0-9][A-Z0-9_-]*)+)(:(\d+))?\/?/i
		),
		text: new RegExp(/^[a-zA-Z]+$/),
		digits: new RegExp(/^[\d() \.\:\-\+#]+$/),
		isodate: new RegExp(
			/^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/
		),
		ip: new RegExp(/^(1|2)?\d?\d([.](1|2)?\d?\d){3}$/)
	};

	import data from './email_tag_data.json';

	export default {
		name: 'InputEmailTags',
		props: {
			value: {
				groupType: String,
				id: String,
				tagName: String,
				valid: Boolean,
				errorMessage: {type: String, default: ''}
			},
			placeholder: {
				type: String,
				default: ""
			},
			readOnly: {
				type: Boolean,
				default: false
			},
			validate: {
				type: String | Function | Object,
				default: ""
			},
			addTagOnKeys: {
				type: Array,
				default: function () {
					return [
						13, // Return
						188, // Comma ','
					];
				}
			},
			addTagOnBlur: {
				type: Boolean,
				default: true
			},
			limit: {
				type: Number,
				default: -1
			},
			beforeAdding: {
				type: Function
			},
		},
		data() {
			return {
				newTag: "",
				innerTags: [...this.value],
				isInputActive: false,
				cursor: -1,
				showList: false,
				findRows: []
			};
		},
		computed: {
			isLimit: function () {
				return this.limit > 0 && Number(this.limit) === this.innerTags.length;
			}
		},

		watch: {
			value() {
				this.innerTags = [...this.value];
				this.validationState();
			},
			'findRows.length': function () {
				this.showList = this.isAbleToShowList();
			},
		},
		methods: {
			onClickOutside() {
				this.findRows = [];
			},
			selectedRow(row) {
				let obj = {
					tagName: row['name'],
					valid: true,
					groupType: row['type'],
					id: row['id'],
					name: row['name'],
					email: row['email'],
					editable: true,
				}

				let name = '';

				if (row['type'] == 'OUTER') {
					name = row['email']
				} else {
					name = row['name'] + (row['email'] ? ' (' + row['email'] + ')' : '')
				}

				obj['tagName'] = name

				this.innerTags.push(obj);
				this.newTag = '';
				this.findRows = [];
				this.tagChange();
			},
			keyUp() {
				this.$emit('key-up', this.newTag);
				if (this.cursor > 0) {
					this.cursor -= 1;
				}
			},
			keyDown() {
				this.$emit('key-down', this.newTag);
				if (this.cursor < this.findRows.length - 1) {
					this.cursor += 1;
				}
			},
			inputChange() {
				this.showList = this.isAbleToShowList();
				this.cursor = 0;
				this.$emit('changed', this.newTag);
			},
			isAbleToShowList() {
				return (this.newTag || '').length >= 1 && this.findRows.length > 0;
			},
			async find(event) {
				if (!this.newTag) {
					this.findRows = [];
					return;
				}

				try {
					if (this.newTag && this.newTag.length > 0) {
						let response = await this.$axios.post('/drive/getUsersAndGroups/', require('qs').stringify({
							type: 'find',
							keyword: this.newTag
						}))

						if (response['data']['rows'] && response['data']['rows'].length > 0) {
							this.findRows = [];

							for (let row of response['data']['rows']) {
								if (row['email'].startsWith(this.newTag) || row['name'].startsWith(this.newTag)) {
									this.findRows.push(row);
								}
							}
						} else {
							this.findRows = [];
						}
					} else {
						this.findRows = [];
					}
				} catch (e) {
					console.log(e);
				}
			},
			setIconType(row) {
				const type = row['groupType'] ? row['groupType']: row['type'];

				if (type == 'USER') {
					return "ico_pop_user";
				} else if (type == 'USER_GROUP' || type == 'COMPANY_GROUP') {
					return "ico_pop_team";
				} else {
					return "ico_pop_email";
				}
			},
			focusNewTag() {
				if (this.readOnly || !this.$el.querySelector(".new-tag")) {
					return;
				}

				this.$el.querySelector(".new-tag").focus();
			},
			handleInputFocus() {
				this.isInputActive = true;
			},
			handleInputBlur(e) {
				this.isInputActive = false;
				this.addNew(e);
			},
			async addNew(e) {
				const keyShouldAddTag = e ? this.addTagOnKeys.indexOf(e.keyCode) !== -1 : true;
				const typeIsNotBlur = e && e.type !== "blur";

				if ((!keyShouldAddTag && (typeIsNotBlur || !this.addTagOnBlur)) || this.isLimit) {
					if (e['key'] != 'ArrowUp' && e['key'] != 'ArrowDown') {
						await this.find(e);
					}

					return;
				}

				const tag = this.beforeAdding ? await this.beforeAdding(this.newTag, this.findRows, this.cursor) : this.newTag;

				const isValid = await this.validateIfNeeded(tag);

				if ((tag['groupType'] == 'USER' || tag['groupType'] == 'OUTER') && isValid == false) {
					let obj = {
						tagName: this.newTag,
						valid: false,
						groupType: null,
						id: null,
						name: null,
						email: null,
						editable: true,
					}

					this.innerTags.push(obj);
					this.newTag = '';
					this.findRows = [];

					return false;
				}

				if (tag) {
					let isDup = false;
					let name = '';

					if (tag['groupType'] == 'OUTER') {
						name = tag['email']
					} else {
						name = tag['name'] + (tag['email'] ? ' (' + tag['email'] + ')' : '')
					}

					let tagObj = {
						tagName: name,
						valid: tag['valid'],
						groupType: tag['groupType'],
						id: tag['id'],
						name: tag['name'],
						email: tag['email'],
						editable: true,
					};

					for (const row of this.innerTags) {
						if (row['groupType'] == tag['groupType'] && row['id'] == tag['id']) {
							isDup = true;
							break;
						}
					}

					if (isDup == true) {
						this.newTag = '';
						this.findRows = [];
						return false;
					}

					this.innerTags.push(tagObj);
					this.newTag = "";
					this.findRows = [];
					this.tagChange();

					e && e.preventDefault();
				} else {
					if (this.beforeAdding) {
						this.newTag = "";
					}
				}
			},
			validateIfNeeded(tagValue) {
				if (this.validate === "" || this.validate === undefined) {
					return true;
				}

				if (typeof this.validate === "function") {
					return this.validate(tagValue['email']);
				}

				if (typeof this.validate === "string" &&
					Object.keys(validators).indexOf(this.validate) > -1) {
					return validators[this.validate].test(tagValue['email']);
				}

				if (typeof this.validate === "object" &&
					this.validate.test !== undefined) {
					return this.validate.test(tagValue['email']);
				}

				return true;
			},
			remove(index) {
				this.innerTags.splice(index, 1);
				this.validationState();
				this.tagChange();
			},
			removeLastTag(event) {
				if (this.newTag) {
					return;
				}

				this.innerTags.pop();
				this.tagChange();
			},
			tagChange() {
				this.$emit("update:tags", this.innerTags);
				this.$emit("input", this.innerTags);
			},
			validationState() {
				if (this.innerTags == null || this.innerTags.length < 1) {
					this.$parent.errorMessage = '';
				} else {
					let isValid = true;

					for (let i = 0; i < this.innerTags.length; i++) {
						if (this.innerTags[i]['valid'] == false) {
							isValid = false;

							break;
						}
					}

					this.validCheck();

					if (isValid == false) {
						this.$parent.completeInputForm = false;
					} else {
						this.$parent.errorMessage = '';
						this.$parent.completeInputForm = true;
					}
				}
			},
			validCheck() {
				//alert(1)
			}
		}
	};
</script>

<style scoped>
	.tag-wrapper {

	}

	.tag-wrapper .input-tag.error {
		color: #D94748;
		border-color: #D94748;
	}

	.tag-wrapper .input-tag .remove {
		cursor: pointer;
		font-weight: bold;
		color: #638421;
	}

	.tag-wrapper .input-tag .remove:hover {
		text-decoration: none;
	}

	.tag-wrapper .input-tag .remove:empty::before {
		content: " x";
	}

	.tag-wrapper .new-tag {
		background: transparent;
		border: 0;
		color: #777;
		font-size: 13px;
		font-weight: 400;
		margin-bottom: 6px;
		margin-top: 1px;
		outline: none;
		padding: 4px;
		padding-left: 0 !important;
		flex-grow: 1;
		height: 22px !important;
		width: 100%;
	}

	input::placeholder {
		font-size: 12px;

	}

	.tag-wrapper.read-only {
		cursor: default;
	}

	.find-rows {
		position: absolute;
		display: none;
		left: 26px;
		min-width: 120px;
		white-space: nowrap;
		border: solid 1px #B6C2D4;
		background: White;
		border-radius: 5px;
		-webkit-box-shadow: 1.414px 1.414px 2px 0px rgba(0, 0, 0, 0.15);
		box-shadow: 1.414px 1.414px 2px 0px rgba(0, 0, 0, 0.15);
		z-index: 99;
		margin-bottom: 10px;
	}

	.find-rows li {
		padding: 5px;
		cursor: pointer;
	}

</style>

vue.js inputtagemail
