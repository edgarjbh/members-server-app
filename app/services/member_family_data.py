from sqlalchemy.orm import Session

from app.database import MemberFamilyData
from app.database.member_children import MemberChildren
from app.models import FamilyDataResponse, MemberChildrenDataResponse, MemberFamilyDataResponse


class MembersFamilyDataService:
    def __init__(self):
        pass

    def find_by_member_id(self, member_id, db: Session) -> MemberFamilyDataResponse | None:
        member_family_data = db.query(MemberFamilyData).filter(MemberFamilyData.member_id == member_id).first()
        member_family_data_response = None
        if member_family_data:
            member_family_data_response = FamilyDataResponse.model_validate(member_family_data)

        member_children_list = db.query(MemberChildren).filter(MemberChildren.member_id == member_id).all()
        member_children_response = []
        if member_children_list:
            member_children_response = [
                MemberChildrenDataResponse.model_validate(child) for child in member_children_list
            ]

        if not member_family_data_response and not member_children_response:
            return None

        return MemberFamilyDataResponse(
            familyData=member_family_data_response, childrenDataList=member_children_response
        )
