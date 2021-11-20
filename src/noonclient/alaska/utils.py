from noonclient.alaska.model import NoonModel, NoonSpace, NoonStructure


class SpaceCrawler:
    def process_space(noonSpace: NoonSpace):
        pass

class ModelUtils:
    def crawl_model(noonmodel: NoonModel, space_crawler: SpaceCrawler):
        if noonmodel is not None and noonmodel.leases is not None:
            for next in noonmodel.leases:
                if  not (next is None or next.structure is None):
                    ModelUtils.crawl_structure(next.structure, space_crawler)
    
    def crawl_structure(noon_structure: NoonStructure, space_crawler: SpaceCrawler):
        pass