# coding: utf-8
class MergeXml
  attr_accessor :source_xml_path
  attr_accessor :target_xml_path

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
    end

    File.open(self.target_xml_path, 'w+') do |f|
      f.puts target_doc.write('', 2).join('').gsub("/><", "/>\n<").gsub("><", ">\n<").gsub("\n\n", "\n")
      f.close
    end

  end


  private

  #+nodename+: source_xml_item 下的 名字为 +nodename+的节点
  def merge_node(source_xml_item, target_xml_item, node_name)
    source_xml_item.get_elements(node_name).each do |node|
      meta_name = node.attributes['android:name'] || node.attributes['name']
      if target_xml_item.get_elements("#{node_name}[@android:name='#{meta_name}']").empty? &&
          target_xml_item.get_elements("#{node_name}[@name='#{meta_name}']").empty?
        target_xml_item.add_element node
        puts "#{node_name}\t#{meta_name}"
      end
    end
  end

end