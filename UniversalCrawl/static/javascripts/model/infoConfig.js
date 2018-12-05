(function () {
    var infoConfig = {
        dataStore: {
            treeObj: {},
            editIndex: "",
            //数据获取网页链接
            ajaxUrl: "",
            docWidth: 0,
            docHeight: 0
        },
        /**
         * 初始化
         * @return {[type]} [description]
         */
        init: function () {
            this.dataStore.docWidth = $(document).width();
            this.dataStore.docHeight = $(document).height();
            this.initTree();
            this.initGrid();
            this.dataStore.ajaxUrl = location.protocol + "//" + location.host + "/config";
            this.initEvent();
        },
        /**
         * 初始化分类树
         * @return {[type]} [description]
         */
        initTree: function () {
            var that = this;
            var setting = {
                data: {
                    simpleData: {
                        enable: true,
                        idKey: "_id"
                    }
                },
                callback: {
                    onRightClick: function (event, treeId, treeNode) {
                        that.dataStore.treeObj.selectNode(treeNode);
                        $('#mm_p').menu('show', {
                            left: event.clientX,
                            top: event.clientY
                        });
                    },
                    onClick: function (event, treeId, treeNode, clickFlag) {
                        var sSite = treeNode.site;
                        that.loadGridData(sSite);
                    }
                }
            };
            //获取分类信息
            var sUrl = location.protocol + "//" + location.host + "/config",
                param = {
                    type: "cate"
                };

            this.SendAjaxReq4Json(sUrl, param, sucFunc, errFunc);

            function sucFunc(dataInfo) {
                if (dataInfo.state == "ok") {
                    exp.ztreeHelper.initTree('cateTree', setting, dataInfo.objList);
                    that.dataStore.treeObj = exp.ztreeHelper.getTreeObj('cateTree');
                } else {
                    alert(dataInfo.msg);
                }
            }

            function errFunc(msgInfo) {
                var s = msgInfo;
            }
        },
        initEvent: function () {
            var that = this;
            $(".grap").live("click", function (e) {
                var urlList = [],
                    dom = $(e.target),
                    sUrl = dom.attr("_id"),
                    sSrc = dom.attr("src"),
                    sRemark = dom.attr("remark");

                var urlObj = {
                    url: sUrl,
                    src: sSrc,
                    remark: sRemark
                };
                urlList.push(urlObj);
                that.grap(urlList);
            });
        },
        loadGridData: function (sSite) {
            var that = this;
            var gridObj = that.dataStore.gridObj;
            var sUrl = that.dataStore.ajaxUrl;
            //如果存在站点信息，则获取该站点下相关配置的网址信息
            if (sSite) {
                var param = {
                    type: "site",
                    site: sSite
                };
                that.SendAjaxReq4Json(sUrl, param, function (dataInfo) {
                    if (dataInfo.state == "ok") {
                        gridObj.datagrid('loadData', {
                            total: dataInfo.objList.length,
                            rows: dataInfo.objList
                        });
                    } else {
                        alert(dataInfo.msg);
                    }
                }, function (msgInfo) {
                    var s = msgInfo;
                });
            }
            //如果非站点节点点击，则清空右边的网址信息
            else {
                gridObj.datagrid('loadData', []);
            }
        },
        /**
         * 新增分类
         */
        addCate: function () {
            this.operCate("add");
        },
        /**
         * 修改分类
         * @return {[type]} [description]
         */
        modCate: function () {
            this.operCate("mod");
        },
        /**
         * 删除分类
         * @return {[type]} [description]
         */
        delCate: function () {
            var that = this,
                treeObj = this.dataStore.treeObj,
                nodes = treeObj.getSelectedNodes(),
                node;
            if (nodes.length > 0) {
                node = nodes[0];
            } else {
                return;
            }

            $.dialog({
                title: "删除确认",
                content: "真的要删除该分类吗?",
                ok: function () {
                    //获取分类信息
                    var sUrl = location.protocol + "//" + location.host + "/config",
                        param = {
                            type: "removeCate",
                            nodeObj: {
                                _id: node._id
                            }
                        };
                    that.SendAjaxReq4Json(sUrl, param, sucFunc, errFunc);
                    return true;
                },
                width: 229,
                height: 60,
                okVal: "确认",
                cancelVal: "取消",
                cancel: true,
                min: 0,
                max: 0,
                resize: 0,
                left: (this.dataStore.docWidth - 229) / 2,
                top: (this.dataStore.docHeight - 60) / 2 - 28
            });

            function sucFunc(dataInfo) {
                if (dataInfo.state == "ok") {
                    treeObj.removeNode(node);
                    alert("删除成功");
                } else {
                    alert(dataInfo.msg);
                }
            }

            function errFunc(msgInfo) {
                var s = msgInfo;
            }
        },
        /**
         * 分类操作
         * @param  {[type]} type 'add':新增,'mod':修改
         * @return {[type]}      [description]
         */
        operCate: function (type) {
            var that = this,
                treeObj = this.dataStore.treeObj,
                nodes = treeObj.getSelectedNodes(),
                node,
                newNode;
            //看是否有节点选中
            if (nodes.length > 0) {
                node = nodes[0];
            } else {
                return;
            }
            //获取分类信息
            var sUrl = location.protocol + "//" + location.host + "/config",
                param = {
                    type: "saveCate"
                };

            var sTypeName = type == "add" ? "新增分类" : "修改分类",
                sName = type == "add" ? "" : " value='" + node.name + "'",
                sHref = type == "add" ? "" : " value='" + node.site + "'",
                sContent = "<div style='margin:5px'><span style='margin-right:15px'>名称:</span><input style='width:300px' type='text' id='inpName' " + sName + "></div>" +
                    "<div style='margin:5px'><span style='margin-right:15px'>网址:</span><input style='width:300px' type='text' id='inpHref' " + sHref + "></div>";
            //跳出对话框
            $.dialog({
                title: sTypeName,
                content: sContent,
                ok: function () {
                    var sCateName = $("#inpName").val(),
                        sSiteUrl = $("#inpHref").val();
                    //alert(sCateName);
                    if (sCateName) {
                        if (type == "add") {
                            var sId = that.guidGenerator();
                            newNode = {
                                _id: sId,
                                pId: node._id,
                                name: sCateName,
                                site: sSiteUrl,
                                isParent: sSiteUrl ? false : true
                            };
                        } else if (type == "mod") {
                            node.name = sCateName;
                            node.site = sSiteUrl;
                            node.isParent = sSiteUrl ? false : true;
                            newNode = {
                                _id: node._id,
                                pId: node.pId,
                                name: sCateName,
                                site: sSiteUrl,
                                isParent: sSiteUrl ? false : true
                            };
                        }
                        param.nodeObj = newNode;
                        //发送请求到服务器端，进行数据库操作
                        that.SendAjaxReq4Json(sUrl, param, sucFunc, errFunc);
                        return true;
                    } else {
                        alert("请输入分类名称");
                        return false;
                    }
                },
                width: 400,
                height: 60,
                okVal: "保存",
                cancelVal: "关闭",
                cancel: true,
                min: 0,
                max: 0,
                resize: 0,
                lock: 1,
                drag: 0,
                left: (this.dataStore.docWidth - 400) / 2,
                top: (this.dataStore.docHeight - 60) / 2 - 28
            });

            function sucFunc(dataInfo) {
                //数据库操作成功后修改树节点信息
                if (dataInfo.state == "ok") {
                    if (type == "add") {
                        treeObj.addNodes(node, dataInfo.objList);
                    } else if (type == "mod") {
                        node.name = dataInfo.objList.name;
                        treeObj.updateNode(node);
                    }
                } else {
                    alert(dataInfo.msg);
                }
            }

            function errFunc(msgInfo) {
                var s = msgInfo;
            }
        },
        initGrid: function () {
            var that = this;
            var colList = [{
                field: 'ck',
                checkbox: true
            }, {
                field: 'src',
                title: '频道',
                width: 100,
                sortable: true,
                //align: 'center',
                editor: 'text'
            }, {
                field: '_id',
                title: '网址',
                width: 360,
                sortable: true,
                //align: 'center',
                editor: 'text'
            }, {
                field: 'Summary',
                title: '属性',
                sortable: true,
                width: 100,
                //align: 'center',
                editor: 'text'
            }, {
                field: 'IsFilter',
                title: '是否过滤',
                sortable: false,
                width: 100,
                editor: 'text'
            }, {
                field: 'ruleName',
                title: '名称',
                sortable: false,
                width: 100,
                editor: 'text'
            }, {
                field: 'operRules',
                title: '操作',
                sortable: false,
                width: 200,
                align: 'center',
                editor: 'text',
                formatter: that.formatAction
            }, {
                field: 'site',
                hidden: 1
            }];

            var toolbarList = [{
                text: '新增',
                iconCls: 'icon-add',
                disabled: false,
                handler: function () {
                    var nodeList = that.dataStore.treeObj.getSelectedNodes();
                    if (nodeList.length > 0) {
                        if (nodeList[0].site) {
                            that.showEditWin('add', nodeList[0].site);
                        } else {
                            alert("非网站节点不允许添加网址！");
                        }
                    } else {
                        alert("请选择分类！");
                    }
                    return;
                }
            }, {
                text: '修改',
                iconCls: 'icon-edit',
                disabled: false,
                handler: function () {
                    that.showEditWin('mod');
                }
            }, {
                text: '删除',
                iconCls: 'icon-remove',
                disabled: false,
                handler: function () {
                    $.dialog({
                        title: "删除确认",
                        content: "真的要删除吗?",
                        ok: function () {
                            var gridObj = that.dataStore.gridObj,
                                sUrl = that.dataStore.ajaxUrl,
                                checkedList = gridObj.datagrid('getChecked'),
                                iCount = checkedList.length,
                                objList = [];

                            for (var i = 0; i < iCount; i++) {
                                objList.push({
                                    _id: checkedList[i]._id
                                });
                            }

                            var param = {
                                type: "removeSite",
                                objInfo: checkedList[0]
                            };

                            that.SendAjaxReq4Json(sUrl, param, function (dataInfo) {
                                if (dataInfo.state == "ok") {
                                    for (var i = iCount - 1; i >= 0; i--) {
                                        var index = gridObj.datagrid('getRowIndex', checkedList[i]);
                                        gridObj.datagrid('deleteRow', index);
                                    }
                                    alert("删除成功!");
                                } else {
                                    alert(dataInfo.msg);
                                }
                            }, function (msgInfo) {

                            });
                        },
                        width: 229,
                        height: 60,
                        okVal: "确认",
                        cancelVal: "取消",
                        cancel: true,
                        min: 0,
                        max: 0,
                        resize: 0,
                        left: (that.dataStore.docWidth - 229) / 2,
                        top: (that.dataStore.docHeight - 60) / 2 - 28
                    });
                }
            }];

            this.dataStore.gridObj = $('#siteInfo').datagrid({
                checkOnSelect: true,
                selectOnCheck: true,
                nowrap: true,
                striped: true,
                //pageSize: 1,
                //pageList: [100, 80, 60, 40, 20, 10,1],
                //pagination: true,
                idField: '_id',
                columns: [colList],
                rownumbers: true,
                singleSelect: false,
                toolbar: toolbarList,
                onDblClickRow: function (index, row) {
                    that.showEditWin('mod');
                },
                onSelect: function (index, row) {

                }
            });
        },
        endEditing: function () {
            var that = this;
            if (that.dataStore.editIndex == undefined) {
                return true;
            }
            var gridObj = that.dataStore.gridObj;
            if (gridObj.datagrid('validateRow', that.dataStore.editIndex)) {
                gridObj.datagrid('endEdit', that.dataStore.editIndex);
                that.dataStore.editIndex = undefined;
                return true;
            } else {
                return false;
            }
        },
        showEditWin: function (operType, siteUrl) {
            var that = this,
                sTypeName = "",
                sSrc = "",
                sHref = "",
                sRuleName = "",
                sSite = siteUrl ? siteUrl : "",
                sRemark = "",
                sContent = "",
                sDisabled = "";

            if (operType == "add") {
                sTypeName = "新增配置信息";
                sRemark = "<select style='width:300px' id='selRemark'>";
                for (var i = 0; i < typeInfo_config.length; i++) {
                    sRemark += "<option value='" + typeInfo_config[i].pbotype + "'>" + typeInfo_config[i].pbotypename + "</option>";
                }
                sRemark += "</select>";
                sIsFilter = "<select style='width:300px' id='isFilter'><option value='是'>是</option><option value='否'>否</option></select>";
            } else {
                sTypeName = "修改配置信息";
                sDisabled = "disabled='disabled'";
                var gridObj = this.dataStore.gridObj;
                var selectedRow = gridObj.datagrid('getSelected');
                if (selectedRow) {
                    sSite = selectedRow.site;
                    sSrc = "value='" + selectedRow.src + "'";
                    sHref = "value='" + selectedRow._id + "'";
                    sRuleName = "value='" + selectedRow.ruleName + "'";
                    sRemark = "<select style='width:300px' id='selRemark'>";
                    for (var i = 0; i < typeInfo_config.length; i++) {
                        sRemark += "<option value='" + typeInfo_config[i].pbotype + "'>" + typeInfo_config[i].pbotypename + "</option>";
                    }
                    sRemark += "</select>";
                    var sTmpReg = "/^(.*?)('" + selectedRow.remark + "')(.*)$/";
                    sRemark = sRemark.replace(eval(sTmpReg), "$1$2 selected $3");
                    sIsFilter = "<select style='width:300px' id='isFilter'><option value='是'>是</option><option value='否'>否</option></select>";
                    var sTmpRegScr = "/^(.*?)('" + selectedRow.IsFilter + "')(.*)$/";
                    sIsFilter = sIsFilter.replace(eval(sTmpRegScr), "$1$2 selected $3");
                    var sTmpRegEnable = "/^(.*?)('" + selectedRow.isEnable + "')(.*)$/";
                } else {
                    alert("请选择需要修改的对象");
                    return;
                }
            }
            sContent = "<div style='margin:5px'><span style='margin-right:15px'>频道:</span><input style='width:300px' type='text' id='inpSrc' " + sSrc + "></div>" +
                "<div style='margin:5px'><span style='margin-right:15px'>网址:</span><input " + sDisabled + " style='width:300px' type='text' id='inpHref' " + sHref + "></div>" +
                "<div style='margin:5px'><span style='margin-right:15px'>名称:</span><input style='width:300px' type='text' id='inpRuleName' " + sRuleName + "></div>" +
                "<div style='margin:5px'><span style='margin-right: 15px;'>属性:</span>" + sRemark + "</div>" +
                "<div style='margin:5px'><span style='margin-right: 15px;'>过滤:</span>" + sIsFilter + "</div>";

            $.dialog({
                title: sTypeName,
                content: sContent,
                ok: function () {
                    var nodeList = that.dataStore.treeObj.getSelectedNodes();
                    var sSrc = $("#inpSrc").val();
                    var sHref = $("#inpHref").val();
                    var sRuleName = $("#inpRuleName").val();
                    var sRemark = $("#selRemark").val();
                    var sSummary = $("#selRemark").find("option:selected").text();
                    var sIsFilter = $("#isFilter").val();
                    var param = {},
                        sSiteName = "";
                    //判断添加的网址是否是属于这个网站的，是允许添加，不是不允许添加
                    if (sHref.indexOf(sSite) >= 0) {
                        var sUrl = location.protocol + "//" + location.host + "/config";
                        //判断是否都填全了
                        if (sSrc && sHref && sRuleName && sRemark) {
                            if (nodeList.length > 0) {
                                sSiteName = nodeList[0].name;
                            }
                            param = {
                                type: "saveSite",
                                objInfo: {
                                    _id: sHref,
                                    src: sSrc,
                                    ruleName: sRuleName,
                                    remark: sRemark,
                                    Summary: sSummary,
                                    site: sSite,
                                    siteName: sSiteName,
                                    IsFilter: sIsFilter
                                }
                            };
                            //发送请求到服务器端，进行数据库操作
                            that.SendAjaxReq4Json(sUrl, param, sucFunc, errFunc);
                            return true;
                        } else {
                            alert("请完善未填项！");
                            return false;
                        }
                    } else {
                        alert("您当前添加的网址并不属于该网站!");
                        return false;
                    }
                },
                width: 400,
                height: 60,
                okVal: "保存",
                cancelVal: "关闭",
                cancel: true,
                min: 0,
                max: 0,
                resize: 0,
                lock: 1,
                left: (this.dataStore.docWidth - 400) / 2,
                top: (this.dataStore.docHeight - 60) / 2 - 28
            });

            function sucFunc(dataInfo) {
                //数据库操作成功后修改树节点信息
                if (dataInfo.state == "ok") {
                    var gridObj = that.dataStore.gridObj;
                    if (operType == "add") {
                        gridObj.datagrid('appendRow', dataInfo.objInfo);
                    } else if (operType == "mod") {
                        var selectedRow = gridObj.datagrid('getSelected');
                        var index = gridObj.datagrid('getRowIndex', selectedRow);
                        gridObj.datagrid('updateRow', {
                            index: index,
                            row: dataInfo.objList
                        });
                    }
                } else {
                    alert(dataInfo.msg);
                }
            }

            function errFunc(msgInfo) {
                var s = msgInfo;
            }
        },
        EditXPath: function (rowIndex) {
            var that = this,
                sTypeName = "编辑抓取规则xpath",
                sitename = "",
                orgsrc = "",
                rulename = "",
                allow_domains = "",
                sContent = "",
                start_urls = "",
                allow_url = "",
                extract_from = "",
                title_xpath = "",
                srcurl_xpath = "",
                datetime_xpath = "",
                datetime_re = "",
                author_xpath = "",
                author_re = "",
                content_xpath = "",
                src_xpath = "",
                src_re = "",
                summary_guid = "",
                sIsFilter = "";

            var gridObj = this.dataStore.gridObj;
            var rowData = gridObj.datagrid('getRows')[rowIndex];

            summary_guid = rowData.remark;
            sIsFilter = rowData.IsFilter;
            sitename = rowData.siteName;
            rulename = rowData.ruleName;
            orgsrc = rowData.src;
            // allow_domains = rowData.site;
            start_urls = rowData._id;
            var spiderType = '<select style="width:300px" id="spiderType"><option value="Universal" selected>通用</option><option value="AjaxSpider">Ajax</option><option value="WeChatSpider">微信</option></select>';
            sRemark = "<select style='width:300px' id='selRemark'>";
            for (var i = 0; i < typeInfo_config.length; i++) {
                sRemark += "<option value='" + typeInfo_config[i].pbotype + "'>" + typeInfo_config[i].pbotypename + "</option>";
            }
            sRemark += "</select>";
            var sTmpReg = "/^(.*?)('" + rowData.remark + "')(.*)$/";
            sRemark = sRemark.replace(eval(sTmpReg), "$1$2 selected $3");
            var param = {
                type: "GetXpath",
                rulename: rulename
            };
            var sUrl = location.protocol + "//" + location.host + "/editxpath";
            that.SendAjaxReq4Json(sUrl, param, function (dataInfo) {
                if (dataInfo != "") {
                    rulename = rulename;
                    allow_url = dataInfo.allow_url;
                    allow_domains = dataInfo.allowed_domains;
                    // extract_from = dataInfo.extract_from.replace(/\"/g, "&quot;");
                    title_xpath = dataInfo.item.attrs.title[0].args[0].replace(/\"/g, "&quot;");
                    srcurl_xpath = dataInfo.item.attrs.srcUrl[0].args[0].replace(/\"/g, "&quot;");
                    datetime_xpath = dataInfo.item.attrs.datetime[0].args[0].replace(/\"/g, "&quot;");
                    datetime_re = dataInfo.item.attrs.datetime[0].re;
                    // author_xpath = dataInfo.item.attrs.author[0].args.replace(/\"/g, "&quot;");
                    // author_re = dataInfo.item.attrs.author[0].re;
                    content_xpath = dataInfo.item.attrs.content[0].args[0].replace(/\"/g, "&quot;");
                    src_xpath = dataInfo.item.attrs.src[0].args[0].replace(/\"/g, "&quot;");
                    src_re = dataInfo.item.attrs.src[0].re;
                }
            }, function (msg) {
                alert(msg);
            }, '', false)

            sContent = "<div style='margin:5px'><label style='margin-right: 15px;'>爬虫类别:</label>" + spiderType + "</div>" +
                "<div style='margin:5px'><label style='margin-right: 15px;'>网站名称:</label><input style='width:300px' type='text' readonly='readonly' id='inpSiteName' value=" + sitename + "></div>" +
                "<div style='margin:5px'><label style='margin-right: 15px;'>频道:</label><input style='width:300px' type='text' readonly='readonly' id='inpOrgSrc' value=" + orgsrc + "></div>" +
                "<div style='margin:5px'><label for='inpRuleName' style='margin-right:15px;'>名称:</label><input style='width:300px' type='text' readonly='readonly' id='inpRuleName' value=" + rulename + "></div>" +
                "<div style='margin:5px'><label style='margin-right: 15px;'>域名:</label><input style='width:300px' type='text' id='inpAllowDomains' value=" + allow_domains + "></div>" +
                "<div style='margin:5px'><label style='margin-right: 15px;'>起始URL:</label><input style='width:300px' type='text' id='inpStartUrls' value=" + start_urls + "></div>" +
                // "<div style='margin:5px'><label for='inpAllowUrl' style='margin-right: 15px;'>链接规则:</label><input style='width:300px' type='text' id='inpAllowUrl' value=" + allow_url + "></div>" +
                // "<div style='margin:5px'><label for='inpExtractFrom' style='margin-right: 15px;'>提取区域:</label><input style='width:300px' type='text' id='inpExtractFrom' value=\"" + extract_from + "\"></div>" +
                "<div style='margin:5px'><label for='inpTitleXpath' style='margin-right: 15px;'>标题:</label><select style='width:60px' id='inpTitleGetType'><option value='xpath' selected=''>xpath</option><option value='css'>css</option><option value='value'>value</option><option value='attr'>attr</option></select><input style='width:300px' type='text' id='inpTitleXpath' value=\"" + title_xpath + "\"></div>" +
                "<div style='margin:5px'><label for='inpSrcUrlXpath' style='margin-right: 15px;'>链接:</label><select style='width:60px' id='inpSrcUrlGetType'><option value='xpath'>xpath</option><option value='css'>css</option><option value='value'>value</option><option value='attr' selected=''>attr</option></select><input style='width:300px' type='text' id='inpSrcUrlXpath' value=\"" + srcurl_xpath + "\"></div>" +
                "<div style='margin:5px'><label for='inpDatetimeXpath' style='margin-right: 15px;'>日期:</label><select style='width:60px' id='inpDatetimeGetType'><option value='xpath' selected=''>xpath</option><option value='css'>css</option><option value='value'>value</option><option value='attr'>attr</option></select><input style='width:300px' type='text' id='inpDatetimeXpath' value=\"" + datetime_xpath + "\"></div>" +
                "<div style='margin:5px'><label for='inpDatetimeReXpath' style='margin-right: 15px;'>日期规则:</label><input style='width:300px' type='text' id='inpDatetimeReXpath' value=" + datetime_re + "></div>" +
                "<div style='margin:5px'><label for='inpAuthorXpath' style='margin-right: 15px;'>作者:</label><select style='width:60px' id='inpAuthorGetType'><option value='xpath' selected=''>xpath</option><option value='css'>css</option><option value='value'>value</option><option value='attr'>attr</option></select><input style='width:300px' type='text' id='inpAuthorXpath' value=\"" + author_xpath + "\"></div>" +
                "<div style='margin:5px'><label for='inpAuthorReXpath' style='margin-right: 15px;'>作者规则:</label><input style='width:300px' type='text' id='inpAuthorReXpath' value=" + author_re + "></div>" +
                "<div style='margin:5px'><label for='inpContentXpath' style='margin-right: 15px;'>内容:</label><select style='width:60px' id='inpContentGetType'><option value='xpath' selected=''>xpath</option><option value='css'>css</option><option value='value'>value</option><option value='attr'>attr</option></select><input style='width:300px' type='text' id='inpContentXpath' value=\"" + content_xpath + "\"></div>" +
                "<div style='margin:5px'><label for='inpSrcXpath' style='margin-right: 15px;'>来源:</label><select style='width:60px' id='inpSrcGetType'><option value='xpath' selected=''>xpath</option><option value='css'>css</option><option value='value'>value</option><option value='attr'>attr</option></select><input style='width:300px' type='text' id='inpSrcXpath' value=\"" + src_xpath + "\"></div>" +
                "<div style='margin:5px'><label for='inpSrcReXpath' style='margin-right: 15px;'>来源规则:</label><input style='width:300px' type='text' id='inpSrcReXpath' value=" + src_re + "></div>";

            $.dialog({
                title: sTypeName,
                content: sContent,
                ok: function () {
                    var nodeList = that.dataStore.treeObj.getSelectedNodes();
                    var sSpiderType = $("#spiderType").val();
                    var sRulename = $("#inpRuleName").val();
                    var sAllowdomains = $("#inpAllowDomains").val();
                    var sStarturls = $("#inpStartUrls").val();
                    // var sAllowurl = $("#inpAllowUrl").val();
                    // var sExtractfrom = $("#inpExtractFrom").val();
                    var sTitleGetType = $("#inpTitleGetType").val();
                    var sTitlexpath = $("#inpTitleXpath").val();
                    var sSrcUrlGetType = $("#inpSrcUrlGetType").val();
                    var sSrcUrlxpath = $("#inpSrcUrlXpath").val();
                    var sSrcGetType = $("#inpSrcGetType").val();
                    var sSrcxpath = $("#inpSrcXpath").val();
                    var sSrcre = $("#inpSrcReXpath").val();
                    var sDatetimeGetType = $("#inpDatetimeGetType").val();
                    var sDatetimexpath = $("#inpDatetimeXpath").val();
                    var sDatetimere = $("#inpDatetimeReXpath").val();
                    var sAuthorGetType = $("#inpAuthorGetType").val();
                    var sAuthorxpath = $("#inpAuthorXpath").val();
                    var sAuthorre = $("#inpAuthorReXpath").val();
                    var sContentGetType = $("#inpContentGetType").val();
                    var sContentxpath = $("#inpContentXpath").val();
                    var param = {};
                    var sUrl = location.protocol + "//" + location.host + "/editxpath";
                    //判断是否都填全了
                    if (sRulename && sAllowdomains && sStarturls && sTitlexpath && sDatetimexpath && sContentxpath) {
                        param = {
                            type: "EditXPath",
                            spidertype: sSpiderType,
                            rulename: sRulename,
                            allow_domains: sAllowdomains,
                            start_urls: sStarturls,
                            // allow_url: sAllowurl,
                            // extract_from: sExtractfrom,
                            titleGetType: sTitleGetType,
                            title_xpath: sTitlexpath,
                            srcUrlGetType: sSrcUrlGetType,
                            srcUrl_xpath: sSrcUrlxpath,
                            srcGetType: sSrcGetType,
                            src_xpath: sSrcxpath,
                            src_re: sSrcre,
                            datetimeGetType: sDatetimeGetType,
                            datetime_xpath: sDatetimexpath,
                            datetime_re: sDatetimere,
                            authorGetType: sAuthorGetType,
                            author_xpath: sAuthorxpath,
                            author_re: sAuthorre,
                            contentGetType: sContentGetType,
                            content_xpath: sContentxpath,
                            orgsrc: orgsrc,
                            siteName: sitename,
                            summary: summary_guid,
                            isFilter: sIsFilter
                        };
                        //发送请求到服务器端，进行数据库操作
                        that.SendAjaxReq4Json(sUrl, param, sucFunc, errFunc);
                        return true;
                    } else {
                        alert("请完善未填项！");
                        return false;
                    }
                },
                width: 800,
                height: 400,
                okVal: "保存",
                cancelVal: "关闭",
                cancel: true,
                min: 0,
                max: 0,
                resize: 0,
                lock: 1,
                left: (this.dataStore.docWidth - 800) / 2,
                top: (this.dataStore.docHeight - 500) / 2
            });

            function sucFunc(dataInfo) {
                //数据库操作成功后修改树节点信息

            }

            function errFunc(msgInfo) {
                var s = msgInfo;
            }
        },
        grap: function (urlList) {
            var sUrl = location.protocol + "//" + location.host + "/grap",
                param = {
                    urlList: urlList
                };
            this.SendAjaxReq4Json(sUrl, param, sucFunc, errFunc, "post");

            function sucFunc(dataInfo) {
                alert("抓取已经开始!");
            }

            function errFunc(msgInfo) {
                var s = msgInfo;
            }
        },
        formatAction: function (value, rowData, rowIndex) {
            var actionStr = '<a title="修改" href="javascript:void(0)" onClick="ModObj.EditXPath(\'' + rowIndex + '\')">修改配置</a> | ';
            if (rowData.isEnable == "0") {
                actionStr += '<a title="开关" href="javascript:void(0)" onClick="ModObj.EditEnable(\'' + rowIndex + '\')">启用</a>';
            }
            else {
                actionStr += '<a title="开关" href="javascript:void(0)" onClick="ModObj.EditEnable(\'' + rowIndex + '\')">禁用</a>';
            }
            return actionStr;
        },
        EditEnable: function (rowIndex) {
            var that = this;
            var sUrl = location.protocol + "//" + location.host + "/config";
            var gridObj = this.dataStore.gridObj;
            var rowData = gridObj.datagrid('getRows')[rowIndex];
            if (rowData.sisEnable == "1") {
                rowData.sisEnable = "0";
            } else {
                rowData.sisEnable = "1";
            }
            var param = {
                type: "saveSite",
                objInfo: {
                    _id: rowData.sHref,
                    src: rowData.sSrc,
                    remark: rowData.sRemark,
                    Summary: rowData.sSummary,
                    site: rowData.sSite,
                    siteName: rowData.sSiteName,
                    IsFilter: rowData.sIsFilter,
                    isEnable: rowData.sisEnable
                }
            }
            that.SendAjaxReq4Json(sUrl, param, function (dataInfo) {
                var sSite = rowData.site;
                that.loadGridData(sSite);
            }, function (msg) {
                alert(msg);
            }, '', false)
        }
    };

    exp.ModObj = infoConfig;

})();

window.ModObj = imp(["genTools", "getDataTools", "dataTools", "ModObj"]);

$(function () {
    ModObj.init();
});