# coding: utf-8
class MergeXml
  attr_accessor :source_xml_path
  attr_accessor :target_xml_path

  PUBLIC_ID_VALUES = {attr: 0x7f010000, drawable: 0x7f020000}

  def initialize(source_xml_path, target_xml_path)
    self.source_xml_path = source_xml_path
    self.target_xml_path = target_xml_path
    self.start
  end

  def start
    src_doc = REXML::Document.new(File.read("#{self.source_xml_path}"))
    target_doc = REXML::Document.new(File.new(self.target_xml_path))

    root_doc_name = src_doc.root.name #跟节点的名称

    #AndroidManifest
    if root_doc_name=='manifest'
      %w(uses-permission permission).each do |node_name|
        merge_node(src_doc.root, target_doc.root, node_name)
      end

      src_app_item = src_doc.root.elements['application']
      target_app_item = target_doc.root.elements['application']
      %w(meta-data activity service receiver provider).each do |node_name|
        merge_node(src_app_item, target_app_item, node_name)
      end
    end

    if root_doc_name=='resources'
      #strings.xml etc.
      %w(string attr bool color dimen integer style).each do |res|
        if self.source_xml_path.end_with?("#{res}s.xml")
          merge_node(src_doc.root, target_doc.root, res)
        end
      end

      #string-arrays.xml drawables.xml ids.xml
      if self.source_xml_path.end_with?('arrays.xml')
        merge_node(src_doc.root, target_doc.root, 'string-array')
      elsif self.source_xml_path.end_with?('drawables.xml')
        merge_node(src_doc.root, target_doc.root, 'item')
      elsif self.source_xml_path.end_with?('ids.xml')
        merge_node(src_doc.root, target_doc.root, 'item')
      end
      save_target_xml(target_doc)

      #public .xml
      if self.source_xml_path.end_with?('public.xml')
        merge_public_xml
      end
    end

  end

  private

  # id:0x7f010000
  # drawable 从 .....1 开始
  # anim attr array bool color dimen drawable id integer layout mipmap raw string style
  def public_id_value(type=:drawable)
    if PUBLIC_ID_VALUES.keys.include?(type)
      PUBLIC_ID_VALUES[type] = PUBLIC_ID_VALUES[type].to_i+1
    else
      PUBLIC_ID_VALUES[type]=(((PUBLIC_ID_VALUES[PUBLIC_ID_VALUES.keys.last]/(16*16*16*16))+1)*(16*16*16*16))
    end
    "0x#{PUBLIC_ID_VALUES[type].to_s(16)}"
  end

  # merge public.xml
  def merge_public_xml

    #merge node
    merge_public_node

    #fix id number
    target_doc = REXML::Document.new(File.new(self.target_xml_path))
    target_root = target_doc.root

    target_root.get_elements('public').each do |node|
      type = node.attributes['type'].to_s.to_sym
      name = node.attributes['name'].to_s
      node.delete_attribute('id')
      id = public_id_value(type)
      node.add_attribute('id', id)
      puts "merge public fix :#{type.to_s}\t#{name.to_s}\t#{id}"
    end
    save_target_xml(target_doc)

  end

  #保存目标xml
  def save_target_xml(target_doc)
    File.open(self.target_xml_path, 'w+') do |f|
      f.puts target_doc.write('', 2).join('').gsub("/><", "/>\n<").gsub("><", ">\n<").gsub("\n\n", "\n")
      f.close
    end
  end

  #合并两个public的node（id不改变）
  def merge_public_node
    target_doc = REXML::Document.new(File.new(self.target_xml_path))
    target_root = target_doc.root

    #一次性读取需要检索的target public.xml中的值到内存
    target_id_nodes = {}
    target_root.get_elements('public').each do |node|
      name = node.attributes['name']
      type= node.attributes['type']
      target_id_nodes["name=#{name} type=#{type}"] = true
    end

    #merge
    REXML::Document.new(File.new(self.source_xml_path)).root.get_elements('public').each do |node|
      name = node.attributes['name']
      type= node.attributes['type']
      # if target_root.get_elements("public[@name='#{name}'] and @type='#{type}'").empty?
      unless target_id_nodes["name=#{name} type=#{type}"]
        puts "merge public add :#{type.to_s}\t#{name.to_s}"
        target_root.add node
      end
    end
    save_target_xml(target_doc)
  end

  #+nodename+: source_xml_item 下的 名字为 +nodename+的节点
  def merge_node(source_xml_item, target_xml_item, node_name)

    #一次性读取需要检索的target public.xml中的值到内存
    target_id_nodes = {}
    target_xml_item.get_elements(node_name).each do |node|
      name = node.attributes['name']
      name = node.attributes['android:name'] if name.nil? || name == ''
      target_id_nodes["name=#{name}"] = true
    end


    source_xml_item.get_elements(node_name).each do |node|
      meta_name = node.attributes['android:name'] || node.attributes['name']
      #if target_xml_item.get_elements("#{node_name}[@android:name='#{meta_name}']").empty? &&
      #   target_xml_item.get_elements("#{node_name}[@name='#{meta_name}']").empty?
      #target_xml_item.add_element node
      # puts "#{node_name}\t#{meta_name}"
      #end
      name = node.attributes['name']
      name = node.attributes['android:name'] if name.nil? || name == ''
      unless target_id_nodes["name=#{name}"]
        target_xml_item.add_element node
        puts "#{node_name}\t#{meta_name}"
      end
    end
  end

end