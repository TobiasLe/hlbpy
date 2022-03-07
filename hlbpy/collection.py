import bpy
from .base import HighLevelBase
from .base_object import HighLevelObject


class Collection(HighLevelBase):
    def __init__(self, name="Collection", bpy_object=None, reuse=True, clear=False):
        self.objects = []
        self.objects_in_hierarchy = []

        if bpy_object is None:
            already_present = name in [c.name for c in bpy.data.collections]
            if reuse and already_present:
                self.bpy_object = bpy.data.collections[name]
                if not clear:
                    for obj in self.bpy_object.objects:
                        self.objects.append(HighLevelObject(obj, no_update=True))
                    self.update()
            else:
                self.bpy_object = bpy.data.collections.new(name)

            if already_present and clear:
                while self.bpy_object.objects:
                    bpy.data.objects.remove(self.bpy_object.objects[0])

        else:
            self.bpy_object = bpy_object

    def link(self, obj, hierarchically=True, is_child=False):
        try:
            bpy_object = obj.bpy_object
        except AttributeError:
            bpy_object = obj

        if isinstance(obj, Collection):
            try:
                self.bpy_object.children[bpy_object.name]
            except KeyError:
                self.bpy_object.children.link(bpy_object)
        else:
            if not is_child:
                self.objects.append(obj)
            self.objects_in_hierarchy.append(obj)
            self.bpy_object.objects.link(obj.bpy_object)
            obj.linked_collections.append(self)

            if hierarchically:
                for child in obj.children:
                    self.link(child, hierarchically, is_child=True)
        return obj

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]

    def __iter__(self):
        return self.objects.__iter__()
